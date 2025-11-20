import streamlit as st
import pandas as pd
import numpy as np
import os

# Import our modules
from modules.data_cleaner import DataCleaner
from modules.statistical_analyzer import StatisticalAnalyzer
from modules.outlier_detector import OutlierDetector
from modules.trend_analyzer import TrendAnalyzer
from modules.visualizer import DataVisualizer

# Setup page
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None

# Title
st.title("Data Analysis Dashboard")
st.write("Upload your data to analyze it")

# Sidebar for file upload
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose CSV or Excel file", type=['csv', 'xlsx', 'xls'])

# Sample data button
st.sidebar.subheader("Or use sample data")
if st.sidebar.button("Load Retail Sales Data"):
    st.session_state.df = pd.read_csv('sample_data/retail_sales_dataset.csv')
    st.sidebar.success("Retail sales data loaded!")

# Load uploaded file
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            st.session_state.df = pd.read_csv(uploaded_file)
        else:
            st.session_state.df = pd.read_excel(uploaded_file)
        st.sidebar.success("Data loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# Get data from session state
df = st.session_state.df

# Main content
if df is not None:
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Statistics", "Outliers", "Trends", "Visualizations"])
    
    # TAB 1: Overview
    with tab1:
        st.header("Dataset Overview")
        
        # Show basic info
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())
        
        # Show data
        st.subheader("Data Preview")
        st.dataframe(df.head(10))
        
        # Show column info
        st.subheader("Column Information")
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes,
            'Missing': df.isnull().sum(),
            'Unique': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(col_info)
    
    # TAB 2: Statistics
    with tab2:
        st.header("Statistical Analysis")
        
        # Get statistics
        analyzer = StatisticalAnalyzer(df)
        
        # Descriptive stats
        st.subheader("Descriptive Statistics")
        stats = analyzer.descriptive_statistics()
        st.dataframe(stats)
        
        # Correlation
        if len(analyzer.numeric_columns) >= 2:
            st.subheader("Correlation Matrix")
            visualizer = DataVisualizer(df)
            fig = visualizer.plot_correlation_heatmap()
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: Outliers
    with tab3:
        st.header("Outlier Detection")
        
        detector = OutlierDetector(df)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            # Select method and column
            method = st.selectbox("Method", ["IQR", "Z-Score"])
            selected_col = st.selectbox("Select Column", numeric_cols)
            
            if st.button("Detect Outliers"):
                # Detect outliers based on method
                if method == "IQR":
                    outliers = detector.detect_iqr([selected_col])
                    summary = detector.get_outlier_summary('iqr')
                    info = summary['columns'][selected_col]
                else:
                    outliers = detector.detect_zscore([selected_col])
                    summary = detector.get_outlier_summary('zscore')
                    info = summary['columns'][selected_col]
                
                # Show results
                st.write(f"**Found {info['outlier_count']} outliers ({info['outlier_percentage']:.2f}%)**")
                
                # Plot outliers
                visualizer = DataVisualizer(df)
                fig = visualizer.plot_outliers(selected_col, outliers[selected_col])
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: Trends
    with tab4:
        st.header("Trend Analysis")
        
        trend_analyzer = TrendAnalyzer(df)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            # Detect time column
            time_col = trend_analyzer.detect_time_column()
            if not time_col:
                time_col = st.selectbox("Select Time Column", df.columns)
            
            selected_col = st.selectbox("Select Value Column", numeric_cols)
            
            # Get trend
            trend_info = trend_analyzer.identify_trend(selected_col, time_col)
            
            if trend_info:
                st.write(f"Trend Direction: {trend_info['trend_direction']}")
                st.write(f"Total Change: {trend_info['total_change_percent']:.2f}%")
                
                # Plot
                visualizer = DataVisualizer(df)
                fig = visualizer.plot_time_series(time_col, selected_col)
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 5: Visualizations
    with tab5:
        st.header("Visualizations")
        
        visualizer = DataVisualizer(df)
        viz_type = st.selectbox("Chart Type", ["Distribution", "Scatter Plot", "Bar Chart"])
        
        if viz_type == "Distribution":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                col = st.selectbox("Column", numeric_cols)
                fig = visualizer.plot_distribution(col, plot_type='histogram')
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Scatter Plot":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("X-axis", numeric_cols)
                y_col = st.selectbox("Y-axis", numeric_cols, index=1)
                fig = visualizer.plot_scatter(x_col, y_col)
                st.plotly_chart(fig, use_container_width=True)
        
        else:  # Bar Chart
            cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            if cat_cols:
                col = st.selectbox("Column", cat_cols)
                fig = visualizer.plot_categorical(col, plot_type='bar')
                st.plotly_chart(fig, use_container_width=True)

else:
    # Welcome message
    st.info("Please upload a data file or use sample data to get started")
    
    st.write("### Features:")
    st.write("- View dataset overview and statistics")
    st.write("- Detect outliers in your data")
    st.write("- Analyze trends over time")
    st.write("- Create visualizations")

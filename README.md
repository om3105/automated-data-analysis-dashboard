# Automated Data Analysis Dashboard

A Python-based data analysis dashboard built with Streamlit for automated data cleaning, statistical analysis, and visualization.

## Overview

This project is a student learning project that provides an interactive web interface for analyzing datasets. Users can upload CSV or Excel files and perform comprehensive data analysis including cleaning, statistics, outlier detection, trend analysis, and visualization.

## Features

- **Data Upload** - Support for CSV and Excel files
- **Statistical Analysis** - Descriptive statistics, correlation analysis, distribution analysis
- **Outlier Detection** - IQR method, Z-score method, Isolation Forest
- **Trend Analysis** - Time series analysis and moving averages
- **Interactive Visualizations** - Dynamic charts using Plotly
- **Report Generation** - Automated PDF and HTML reports

## Technologies Used

- **Streamlit** - Web interface
- **Pandas** - Data manipulation
- **NumPy** - Numerical operations
- **Plotly** - Interactive visualizations
- **SciPy** - Statistical analysis
- **Scikit-learn** - Machine learning for outlier detection

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the dashboard:
```bash
streamlit run app.py
```

2. Open browser at `http://localhost:8501`

3. Upload your data file or use the sample retail sales data

4. Explore the analysis tabs

## Project Structure

```
Automated Data Analysis Dashboard/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── modules/
│   ├── data_cleaner.py        # Data cleaning module
│   ├── statistical_analyzer.py # Statistical analysis module
│   ├── outlier_detector.py    # Outlier detection module
│   ├── trend_analyzer.py      # Trend analysis module
│   ├── visualizer.py          # Visualization module
│   └── report_generator.py    # Report generation module
└── sample_data/
    └── retail_sales_dataset.csv # Sample retail sales data
```

## Sample Data

The project includes a retail sales dataset with 1,001 transactions containing:
- Transaction details (ID, Date, Customer ID)
- Customer demographics (Gender, Age)
- Product information (Category, Quantity, Price)
- Sales metrics (Total Amount)

## Author

Student Project - Data Analysis Dashboard

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional


class DataVisualizer:
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def plot_distribution(self, column: str, plot_type: str = 'histogram') -> go.Figure:
        if column not in self.df.columns:
            return go.Figure()
        
        if plot_type == 'histogram':
            fig = px.histogram(self.df, x=column, title=f'Distribution of {column}')
        elif plot_type == 'box':
            fig = px.box(self.df, y=column, title=f'Box Plot of {column}')
        elif plot_type == 'violin':
            fig = px.violin(self.df, y=column, title=f'Violin Plot of {column}', box=True)
        else:
            fig = px.histogram(self.df, x=column, title=f'Distribution of {column}')
        
        return fig
    
    def plot_correlation_heatmap(self, method: str = 'pearson') -> go.Figure:
        columns = self.numeric_columns
        
        if len(columns) < 2:
            return go.Figure()
        
        corr_matrix = self.df[columns].corr(method=method)
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}'
        ))
        
        fig.update_layout(title=f'Correlation Heatmap', width=700, height=700)
        return fig
    
    def plot_time_series(self, time_column: str, value_column: str, moving_average: Optional[int] = None) -> go.Figure:
        df_sorted = self.df.sort_values(time_column)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_sorted[time_column],
            y=df_sorted[value_column],
            mode='lines+markers',
            name=value_column
        ))
        
        if moving_average:
            ma = df_sorted[value_column].rolling(window=moving_average).mean()
            fig.add_trace(go.Scatter(
                x=df_sorted[time_column],
                y=ma,
                mode='lines',
                name=f'{moving_average}-period MA',
                line=dict(dash='dash')
            ))
        
        fig.update_layout(title=f'{value_column} over Time', xaxis_title=time_column, yaxis_title=value_column)
        return fig
    
    def plot_scatter(self, x_column: str, y_column: str, color_column: Optional[str] = None, trendline: bool = True) -> go.Figure:
        fig = px.scatter(
            self.df,
            x=x_column,
            y=y_column,
            color=color_column,
            title=f'{y_column} vs {x_column}',
            trendline='ols' if trendline else None
        )
        return fig
    
    def plot_categorical(self, column: str, plot_type: str = 'bar', top_n: Optional[int] = None) -> go.Figure:
        value_counts = self.df[column].value_counts()
        
        if top_n:
            value_counts = value_counts.head(top_n)
        
        if plot_type == 'bar':
            fig = go.Figure(data=[go.Bar(x=value_counts.index, y=value_counts.values)])
            fig.update_layout(title=f'Distribution of {column}', xaxis_title=column, yaxis_title='Count')
        else:
            fig = go.Figure(data=[go.Pie(labels=value_counts.index, values=value_counts.values)])
            fig.update_layout(title=f'Distribution of {column}')
        
        return fig
    
    def plot_outliers(self, column: str, outlier_mask: pd.Series) -> go.Figure:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.df.index[~outlier_mask],
            y=self.df.loc[~outlier_mask, column],
            mode='markers',
            name='Normal',
            marker=dict(color='blue', size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=self.df.index[outlier_mask],
            y=self.df.loc[outlier_mask, column],
            mode='markers',
            name='Outliers',
            marker=dict(color='red', size=10, symbol='x')
        ))
        
        fig.update_layout(title=f'Outliers in {column}', xaxis_title='Index', yaxis_title=column)
        return fig

"""
Configuration settings for the Data Analysis Dashboard
"""

# Data Cleaning Configuration
CLEANING_CONFIG = {
    'missing_value_strategies': ['drop', 'mean', 'median', 'mode', 'forward_fill', 'backward_fill'],
    'default_strategy': 'mean',
}

# Statistical Analysis Configuration
STATS_CONFIG = {
    'confidence_level': 0.95,
    'correlation_methods': ['pearson', 'spearman', 'kendall'],
}

# Outlier Detection Configuration
OUTLIER_CONFIG = {
    'iqr_multiplier': 1.5,
    'zscore_threshold': 3,
    'isolation_forest_contamination': 0.1,
}

# Trend Analysis Configuration
TREND_CONFIG = {
    'moving_average_windows': [7, 14, 30],
}

# Visualization Configuration
VIZ_CONFIG = {
    'color_palette': 'viridis',
    'figure_size': (12, 6),
    'dpi': 100,
    'style': 'darkgrid',
    'plotly_template': 'plotly_dark',
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'page_title': 'Data Analysis Dashboard',
    'page_icon': '📊',
    'layout': 'wide',
    'max_upload_size': 200,
}

# Report Configuration
REPORT_CONFIG = {
    'title': 'Data Analysis Report',
    'author': 'Data Analysis Dashboard',
    'include_visualizations': True,
}

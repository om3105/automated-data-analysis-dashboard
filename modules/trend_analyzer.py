import pandas as pd
import numpy as np
from scipy import stats


class TrendAnalyzer:
    
    def __init__(self, df):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.time_column = None
    
    def detect_time_column(self):
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                self.time_column = col
                return col
            
            if self.df[col].dtype == 'object':
                try:
                    pd.to_datetime(self.df[col])
                    self.time_column = col
                    return col
                except:
                    pass
        
        return None
    
    def identify_trend(self, column, time_column=None):
        if column not in self.numeric_columns:
            return None
        
        if time_column is None:
            time_column = self.time_column or self.detect_time_column()
        
        if time_column is None:
            return None
        
        df_sorted = self.df.sort_values(time_column)
        x = np.arange(len(df_sorted))
        y = df_sorted[column].values
        
        mask = ~np.isnan(y)
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) < 2:
            return None
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
        
        trend_direction = 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
        
        total_change = ((y_clean[-1] - y_clean[0]) / y_clean[0]) * 100 if y_clean[0] != 0 else 0
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value ** 2,
            'p_value': p_value,
            'trend_direction': trend_direction,
            'total_change_percent': total_change
        }
    
    def calculate_moving_average(self, column, window=7):
        if column not in self.numeric_columns:
            return pd.Series()
        
        return self.df[column].rolling(window=window, min_periods=1).mean()

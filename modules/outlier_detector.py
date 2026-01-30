import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy import stats


class OutlierDetector:
    
    def __init__(self, df):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.outliers = {}
    
    # Use IQR method
    def detect_iqr(self, columns=None, multiplier=1.5):
        if columns is None:
            columns = self.numeric_columns
        
        outliers = {}
        for col in columns:
            if col in self.numeric_columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - multiplier * IQR
                upper_bound = Q3 + multiplier * IQR
                outliers[col] = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
        
        self.outliers['iqr'] = outliers
        return outliers
    
    # Use Z-Score method
    def detect_zscore(self, columns=None, threshold=3):
        if columns is None:
            columns = self.numeric_columns
        
        outliers = {}
        for col in columns:
            if col in self.numeric_columns:
                z_scores = np.abs(stats.zscore(self.df[col].dropna()))
                outliers[col] = pd.Series(False, index=self.df.index)
                outliers[col][self.df[col].notna()] = z_scores > threshold
        
        self.outliers['zscore'] = outliers
        return outliers
    
    # Use Isolation Forest (Machine Learning)
    def detect_isolation_forest(self, contamination=0.1):
        if not self.numeric_columns:
            return pd.Series(False, index=self.df.index)
        
        data = self.df[self.numeric_columns].dropna()
        
        if len(data) < 2:
            return pd.Series(False, index=self.df.index)
        
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso_forest.fit_predict(data)
        
        outliers = pd.Series(False, index=self.df.index)
        outliers[data.index] = predictions == -1
        
        self.outliers['isolation_forest'] = outliers
        return outliers
    
    def get_outlier_summary(self, method):
        if method not in self.outliers:
            return {}
        
        outliers = self.outliers[method]
        
        if isinstance(outliers, dict):
            summary = {
                'method': method,
                'columns': {}
            }
            
            for col, mask in outliers.items():
                summary['columns'][col] = {
                    'outlier_count': mask.sum(),
                    'outlier_percentage': (mask.sum() / len(self.df)) * 100
                }
            
            return summary
        else:
            return {
                'method': method,
                'total_outliers': outliers.sum(),
                'outlier_percentage': (outliers.sum() / len(self.df)) * 100
            }
    
    def get_outlier_dataframe(self, method):
        if method not in self.outliers:
            return pd.DataFrame()
        
        outliers = self.outliers[method]
        
        if isinstance(outliers, dict):
            combined_mask = pd.Series(False, index=self.df.index)
            for mask in outliers.values():
                combined_mask = combined_mask | mask
            return self.df[combined_mask]
        else:
            return self.df[outliers]

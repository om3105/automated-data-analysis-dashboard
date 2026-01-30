import pandas as pd
import numpy as np
from scipy import stats


class StatisticalAnalyzer:
    
    def __init__(self, df):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Calculate basic stats
    def descriptive_statistics(self):
        if not self.numeric_columns:
            return pd.DataFrame()
            
        desc_stats = self.df[self.numeric_columns].describe()
        
        additional_stats = pd.DataFrame({
            'variance': self.df[self.numeric_columns].var(),
            'skewness': self.df[self.numeric_columns].skew(),
            'kurtosis': self.df[self.numeric_columns].kurtosis(),
            'range': self.df[self.numeric_columns].max() - self.df[self.numeric_columns].min(),
            'iqr': self.df[self.numeric_columns].quantile(0.75) - self.df[self.numeric_columns].quantile(0.25)
        }).T
        
        desc_stats = pd.concat([desc_stats, additional_stats])
        return desc_stats
    
    def correlation_analysis(self, method='pearson'):
        if len(self.numeric_columns) < 2:
            return pd.DataFrame()
        
        corr_matrix = self.df[self.numeric_columns].corr(method=method)
        return corr_matrix
    
    # Find strong correlations > threshold
    def get_strong_correlations(self, threshold=0.7, method='pearson'):
        corr_matrix = self.correlation_analysis(method=method)
        strong_corr = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) >= threshold:
                    strong_corr.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        corr_val
                    ))
        
        return sorted(strong_corr, key=lambda x: abs(x[2]), reverse=True)
    
    def distribution_analysis(self, column):
        if column not in self.numeric_columns:
            return {}
        
        data = self.df[column].dropna()
        
        if len(data) >= 3 and len(data) <= 5000:
            shapiro_stat, shapiro_p = stats.shapiro(data)
        else:
            shapiro_stat, shapiro_p = None, None
        
        ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
        
        analysis = {
            'mean': data.mean(),
            'median': data.median(),
            'mode': data.mode().values[0] if not data.mode().empty else None,
            'std': data.std(),
            'variance': data.var(),
            'skewness': stats.skew(data),
            'kurtosis': stats.kurtosis(data),
            'is_normal_ks': ks_p > 0.05,
            'min': data.min(),
            'max': data.max()
        }
        
        return analysis

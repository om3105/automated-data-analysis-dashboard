import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from config import CLEANING_CONFIG


class DataCleaner:
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_report = {
            'original_shape': df.shape,
            'operations': [],
            'final_shape': None
        }
    
    def handle_missing_values(self, strategy: str = 'mean', columns: Optional[List[str]] = None) -> pd.DataFrame:
        if columns is None:
            columns = self.df.columns.tolist()
        
        initial_nulls = self.df.isnull().sum().sum()
        
        if strategy == 'drop':
            self.df = self.df.dropna(subset=columns)
        elif strategy == 'mean':
            for col in columns:
                if self.df[col].dtype in ['int64', 'float64']:
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
        elif strategy == 'median':
            for col in columns:
                if self.df[col].dtype in ['int64', 'float64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
        elif strategy == 'mode':
            for col in columns:
                if not self.df[col].mode().empty:
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
        elif strategy == 'forward_fill':
            self.df[columns] = self.df[columns].fillna(method='ffill')
        elif strategy == 'backward_fill':
            self.df[columns] = self.df[columns].fillna(method='bfill')
        
        final_nulls = self.df.isnull().sum().sum()
        
        self.cleaning_report['operations'].append({
            'operation': 'handle_missing_values',
            'strategy': strategy,
            'columns': columns,
            'nulls_removed': initial_nulls - final_nulls
        })
        
        return self.df
    
    def remove_duplicates(self, subset: Optional[List[str]] = None, keep: str = 'first') -> pd.DataFrame:
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        final_rows = len(self.df)
        
        self.cleaning_report['operations'].append({
            'operation': 'remove_duplicates',
            'duplicates_removed': initial_rows - final_rows
        })
        
        return self.df
    
    def convert_data_types(self, type_map: Optional[Dict[str, str]] = None) -> pd.DataFrame:
        if type_map is None:
            type_map = {}
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    try:
                        self.df[col] = pd.to_numeric(self.df[col])
                        type_map[col] = 'numeric'
                    except:
                        try:
                            self.df[col] = pd.to_datetime(self.df[col])
                            type_map[col] = 'datetime'
                        except:
                            type_map[col] = 'string'
        else:
            for col, dtype in type_map.items():
                if col in self.df.columns:
                    try:
                        if dtype in ['int', 'int64']:
                            self.df[col] = self.df[col].astype('int64')
                        elif dtype in ['float', 'float64']:
                            self.df[col] = self.df[col].astype('float64')
                        elif dtype == 'datetime':
                            self.df[col] = pd.to_datetime(self.df[col])
                        elif dtype == 'category':
                            self.df[col] = self.df[col].astype('category')
                    except:
                        pass
        
        self.cleaning_report['operations'].append({
            'operation': 'convert_data_types',
            'conversions': type_map
        })
        
        return self.df
    
    def get_cleaning_report(self) -> Dict:
        self.cleaning_report['final_shape'] = self.df.shape
        self.cleaning_report['rows_removed'] = self.original_df.shape[0] - self.df.shape[0]
        self.cleaning_report['columns_removed'] = self.original_df.shape[1] - self.df.shape[1]
        return self.cleaning_report
    
    def get_cleaned_data(self) -> pd.DataFrame:
        return self.df

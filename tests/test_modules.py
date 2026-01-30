import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.data_cleaner import DataCleaner
from modules.statistical_analyzer import StatisticalAnalyzer
from modules.outlier_detector import OutlierDetector
from modules.trend_analyzer import TrendAnalyzer
from modules.report_generator import ReportGenerator

class TestModules(unittest.TestCase):

    def setUp(self):
        # Create sample data for testing
        data = {
            'A': [1, 2, 3, 4, 5, 100],  # Contains outlier
            'B': [5, 4, 3, 2, 1, 0],
            'C': [1, np.nan, 3, 4, 5, 6],  # Contains missing value
            'Date': pd.date_range(start='1/1/2022', periods=6)
        }
        self.df = pd.DataFrame(data)

    def test_data_cleaner(self):
        cleaner = DataCleaner(self.df)
        cleaned_df = cleaner.handle_missing_values(strategy='mean', columns=['C'])
        self.assertFalse(cleaned_df['C'].isnull().any())
        self.assertAlmostEqual(cleaned_df['C'][1], 3.8, delta=0.1) # Mean of knowns is 3.8

    def test_statistical_analyzer(self):
        analyzer = StatisticalAnalyzer(self.df)
        stats = analyzer.descriptive_statistics()
        self.assertIn('mean', stats.index)
        self.assertIn('std', stats.index)
        # Check if variance was added
        self.assertIn('variance', stats.index)

    def test_outlier_detector_iqr(self):
        detector = OutlierDetector(self.df)
        outliers = detector.detect_iqr(['A'])
        # 100 should be an outlier
        self.assertTrue(outliers['A'].iloc[5]) 
        self.assertFalse(outliers['A'].iloc[0])

    def test_outlier_detector_zscore(self):
        detector = OutlierDetector(self.df)
        outliers = detector.detect_zscore(['A'])
        # 100 should be an outlier (z-score approx 2.0, but threshold default is 3, let's adjust threshold)
        outliers_low_thresh = detector.detect_zscore(['A'], threshold=1.5)
        self.assertTrue(outliers_low_thresh['A'].iloc[5])

    def test_trend_analyzer(self):
        analyzer = TrendAnalyzer(self.df)
        trend_a = analyzer.identify_trend('A', 'Date')
        self.assertEqual(trend_a['trend_direction'], 'increasing')
        
        trend_b = analyzer.identify_trend('B', 'Date')
        self.assertEqual(trend_b['trend_direction'], 'decreasing')

    def test_report_generator_html(self):
        # Just verify it produces a string output
        analysis_mock = {
            'descriptive_stats': self.df.describe(),
            'correlations': [('A', 'B', -0.99)],
            'outliers': {'iqr': pd.Series([False]*6)}
        }
        generator = ReportGenerator(self.df, analysis_mock)
        html_report = generator.generate_html_report()
        self.assertIsInstance(html_report, str)
        self.assertIn('dataset-overview', html_report.lower().replace(' ', '-')) # Simple check

if __name__ == '__main__':
    unittest.main()

import pandas as pd
from fpdf import FPDF
from datetime import datetime
from typing import Dict
from config import REPORT_CONFIG


class ReportGenerator:
    
    def __init__(self, df: pd.DataFrame, analysis_results: Dict):
        self.df = df
        self.analysis_results = analysis_results
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def _add_title_page(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.cell(0, 60, '', 0, 1)
        self.pdf.cell(0, 10, REPORT_CONFIG['title'], 0, 1, 'C')
        
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
        self.pdf.cell(0, 10, f"Author: {REPORT_CONFIG['author']}", 0, 1, 'C')
    
    def _add_section_header(self, title: str):
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, title, 0, 1, 'L')
        self.pdf.ln(5)
    
    def _add_subsection_header(self, title: str):
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 8, title, 0, 1, 'L')
        self.pdf.ln(2)
    
    def _add_text(self, text: str):
        self.pdf.set_font('Arial', '', 10)
        # Handle unicode characters for FPDF (latin-1 only)
        sanitized_text = text.encode('latin-1', 'replace').decode('latin-1')
        self.pdf.multi_cell(0, 6, sanitized_text)
        self.pdf.ln(3)
    
    def _add_dataset_overview(self):
        self.pdf.add_page()
        self._add_section_header('1. Dataset Overview')
        
        overview_text = f"""
Dataset Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns
Total Cells: {self.df.shape[0] * self.df.shape[1]:,}
Memory Usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
Missing Values: {self.df.isnull().sum().sum():,} ({(self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1]) * 100):.2f}%)
Duplicate Rows: {self.df.duplicated().sum():,}
        """
        self._add_text(overview_text.strip())
        
        self._add_subsection_header('Column Information')
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        col_info = f"""
Numeric Columns ({len(numeric_cols)}): {', '.join(numeric_cols[:10])}{'...' if len(numeric_cols) > 10 else ''}
Categorical Columns ({len(categorical_cols)}): {', '.join(categorical_cols[:10])}{'...' if len(categorical_cols) > 10 else ''}
        """
        self._add_text(col_info.strip())
    
    def _add_statistical_summary(self):
        self.pdf.add_page()
        self._add_section_header('2. Statistical Analysis')
        
        if 'descriptive_stats' in self.analysis_results:
            self._add_subsection_header('Descriptive Statistics')
            stats_df = self.analysis_results['descriptive_stats']
            
            for col in stats_df.columns[:5]:
                stats_text = f"""
Column: {col}
  Mean: {stats_df.loc['mean', col]:.2f}
  Median: {stats_df.loc['50%', col]:.2f}
  Std Dev: {stats_df.loc['std', col]:.2f}
  Min: {stats_df.loc['min', col]:.2f}
  Max: {stats_df.loc['max', col]:.2f}
                """
                self._add_text(stats_text.strip())
        
        if 'correlations' in self.analysis_results:
            self._add_subsection_header('Strong Correlations')
            corr_list = self.analysis_results['correlations']
            if corr_list:
                for var1, var2, corr in corr_list[:5]:
                    self._add_text(f"  • {var1} ↔ {var2}: {corr:.3f}")
            else:
                self._add_text("  No strong correlations found")
    
    def _add_outlier_summary(self):
        if 'outliers' not in self.analysis_results:
            return
        
        self.pdf.add_page()
        self._add_section_header('3. Outlier Detection')
        
        outlier_data = self.analysis_results['outliers']
        
        for method, data in outlier_data.items():
            self._add_subsection_header(f'{method.upper()} Method')
            
            if isinstance(data, dict) and 'columns' in data:
                for col, info in data['columns'].items():
                    outlier_text = f"""
Column: {col}
  Outliers Found: {info['outlier_count']} ({info['outlier_percentage']:.2f}%)
                    """
                    self._add_text(outlier_text.strip())
    
    def _add_trend_summary(self):
        if 'trends' not in self.analysis_results:
            return
        
        self.pdf.add_page()
        self._add_section_header('4. Trend Analysis')
        
        trend_data = self.analysis_results['trends']
        
        for col, info in trend_data.items():
            if 'trend' in info and info['trend']:
                trend_info = info['trend']
                trend_text = f"""
Column: {col}
  Direction: {trend_info.get('trend_direction', 'N/A').upper()}
  Total Change: {trend_info.get('total_change_percent', 0):.2f}%
  R-squared: {trend_info.get('r_squared', 0):.3f}
                """
                self._add_text(trend_text.strip())
    
    def _add_recommendations(self):
        self.pdf.add_page()
        self._add_section_header('5. Recommendations')
        
        recommendations = []
        
        missing_pct = (self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1]) * 100)
        if missing_pct > 5:
            recommendations.append(f"• High percentage of missing values ({missing_pct:.2f}%). Consider imputation strategies.")
        
        dup_count = self.df.duplicated().sum()
        if dup_count > 0:
            recommendations.append(f"• Found {dup_count} duplicate rows. Review and remove if necessary.")
        
        if 'outliers' in self.analysis_results:
            recommendations.append("• Outliers detected. Review for data quality issues.")
        
        if 'correlations' in self.analysis_results and self.analysis_results['correlations']:
            recommendations.append("• Strong correlations found between variables.")
        
        if not recommendations:
            recommendations.append("• Dataset appears clean and well-structured.")
        
        for rec in recommendations:
            self._add_text(rec)
    
    def generate_report(self, output_path: str) -> str:
        # Let exceptions bubble up to be caught by the app
        self._add_title_page()
        self._add_dataset_overview()
        self._add_statistical_summary()
        self._add_outlier_summary()
        self._add_trend_summary()
        self._add_recommendations()
        
        self.pdf.output(output_path)
        return output_path
    
    def generate_html_report(self) -> str:
        html = f"""
        <html>
        <head>
            <title>{REPORT_CONFIG['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #1a1a1a; color: #e0e0e0; }}
                h1 {{ color: #4CAF50; }}
                h2 {{ color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 5px; }}
                .metric {{ background-color: #2a2a2a; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                th, td {{ border: 1px solid #444; padding: 8px; text-align: left; }}
                th {{ background-color: #333; }}
            </style>
        </head>
        <body>
            <h1>{REPORT_CONFIG['title']}</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Dataset Overview</h2>
            <div class="metric">
                <p><strong>Shape:</strong> {self.df.shape[0]} rows × {self.df.shape[1]} columns</p>
                <p><strong>Missing Values:</strong> {self.df.isnull().sum().sum()}</p>
                <p><strong>Duplicates:</strong> {self.df.duplicated().sum()}</p>
            </div>
            
            <h2>Data Preview</h2>
            {self.df.head(10).to_html()}
        </body>
        </html>
        """
        
        return html

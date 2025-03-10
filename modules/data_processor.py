import pandas as pd
import numpy as np
import re
import sys
import os

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.data_transformer import DataTransformer

class DataProcessor:
    def __init__(self):
        self.transformer = DataTransformer()
        
    def clean_financial_data(self, data):
        """Clean and standardize financial data."""
        return self.transformer.clean_financial_data(data)
    
    def normalize_metrics(self, df, metrics_list):
        """Extract and normalize specific metrics from data."""
        return self.transformer.normalize_metrics(df, metrics_list)
    
    def calculate_growth_rates(self, df, value_cols, date_col='date'):
        """Calculate period-over-period growth rates."""
        return self.transformer.calculate_growth_rates(df, value_cols, date_col)
    
    def extract_quarterly_trends(self, df, metric_cols, date_col='date'):
        """Extract quarterly trends for specific metrics."""
        return self.transformer.extract_quarterly_trends(df, metric_cols, date_col)
    
    def process_technical_indicators(self, data):
        """Process technical indicators data."""
        return self.transformer.process_technical_indicators(data)

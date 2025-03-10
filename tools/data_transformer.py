import numpy as np
import pandas as pd
import json
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for NumPy and Pandas data types."""
    
    def default(self, obj):
        try:
            if isinstance(obj, (np.integer, np.int64, np.int32)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64, np.float32)):
                return float(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, pd.Timestamp):  # Handle Pandas Timestamp specifically
                return obj.isoformat()
            elif pd.isna(obj):  # Handle NaN/NaT values
                return None
            return super().default(obj)
        except Exception as e:
            logger.error(f"Error in NumpyEncoder: {str(e)}")
            return None

def convert_numpy_types(obj: Any) -> Any:
    """Convert NumPy and Pandas types to Python native types."""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):  # Handle Pandas Timestamp
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy_types(i) for i in obj)
    elif pd.isna(obj):  # Handle NaN/NaT values
        return None
    return obj

def clean_and_convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame and convert columns to appropriate types."""
    if not isinstance(df, pd.DataFrame):
        return df
        
    df_clean = df.copy()
    
    for col in df_clean.columns:
        # First try numeric conversion
        try:
            df_clean[col] = pd.to_numeric(df_clean[col])
            continue
        except (ValueError, TypeError):
            pass
        
        # Then try datetime conversion, with explicit error handling
        try:
            # Try to parse dates with a specific format first
            df_clean[col] = pd.to_datetime(df_clean[col], format='%Y-%m-%d')
        except ValueError:
            try:
                # If that fails, try the default parser
                df_clean[col] = pd.to_datetime(df_clean[col])
            except (ValueError, TypeError):
                # Keep as original if both conversions fail
                pass
    
    return df_clean

def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert DataFrame to list of dicts with serializable types."""
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return []
        
    # Convert to records and handle Timestamps
    records = df.to_dict(orient='records')
    return convert_numpy_types(records)

def prepare_data_for_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare data for report generation."""
    return convert_numpy_types(data)

class DataTransformer:
    """Utility class for cleaning, transforming and standardizing financial data."""
    
    def clean_financial_data(self, data):
        """Clean and standardize financial data."""
        if not data:
            return None
        
        # Convert to DataFrame if it's a list
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data])
        
        # Handle common issues
        for col in df.columns:
            # Convert string numbers to float where possible
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass
                
            # Standardize date formats
            if col.lower().endswith('date'):
                try:
                    df[col] = pd.to_datetime(df[col])
                except (ValueError, TypeError):
                    pass
        
        return df
    
    def normalize_metrics(self, df, metrics_list):
        """Extract and normalize specific metrics from data."""
        result = {}
        
        for metric in metrics_list:
            if metric in df.columns:
                result[metric] = df[metric].tolist()
        
        return result
    
    def calculate_growth_rates(self, df, value_cols, date_col='date'):
        """Calculate period-over-period growth rates."""
        if df is None or df.empty:
            return pd.DataFrame()
        
        # Sort by date
        df = df.sort_values(by=date_col)
        
        # Calculate growth rates for each value column
        for col in value_cols:
            if col in df.columns:
                growth_col = f"{col}_growth"
                df[growth_col] = df[col].pct_change() * 100
        
        return df
    
    def extract_quarterly_trends(self, df, metric_cols, date_col='date'):
        """Extract quarterly trends for specific metrics."""
        if df is None or df.empty or len(df) < 2:
            return {}
        
        # Sort by date
        df = df.sort_values(by=date_col)
        
        trends = {}
        for col in metric_cols:
            if col in df.columns:
                # Calculate quarter-over-quarter change
                qoq_change = df[col].pct_change().iloc[-1] * 100
                
                # Calculate year-over-year change (if we have at least 4 quarters)
                yoy_change = None
                if len(df) >= 5:  # need 5 quarters for 4 quarter comparison
                    yoy_change = ((df[col].iloc[-1] / df[col].iloc[-5]) - 1) * 100
                
                trends[col] = {
                    'current_value': df[col].iloc[-1],
                    'previous_value': df[col].iloc[-2],
                    'qoq_change': qoq_change,
                    'yoy_change': yoy_change
                }
        
        return trends
    
    def process_technical_indicators(self, data):
        """Process technical indicators data."""
        if not data or 'technicalAnalysis' not in data:
            return None
            
        indicators = data['technicalAnalysis']
        df = pd.DataFrame(indicators)
        
        # Process and clean data
        for col in df.columns:
            if col != 'date':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass
        
        try:
            df['date'] = pd.to_datetime(df['date'])
        except (ValueError, TypeError):
            pass
        
        return df.sort_values(by='date')

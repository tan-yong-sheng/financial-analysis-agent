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
            df_clean[col] = pd.to_datetime(df_clean[col], format='%Y-%m-%d', errors='raise')
        except ValueError:
            try:
                # If that fails, try the default parser
                df_clean[col] = pd.to_datetime(df_clean[col], errors='raise')
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
import json
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Union

class NumpyEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for numpy types.
    
    This encoder handles NumPy types that are not natively JSON serializable,
    including numpy.int64, numpy.float64, and numpy arrays. Without this custom
    encoder, JSON serialization will fail with "Object of type int64 is not JSON serializable".
    """
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        return super().default(obj)

def convert_numpy_types(obj: Any) -> Any:
    """
    Convert numpy types to native Python types.
    
    This is a recursive function that walks through nested data structures
    (dicts, lists) and converts any NumPy types to their native Python equivalents.
    This is essential when preparing data for JSON serialization or for sending
    to the LLM, which cannot handle NumPy types directly.
    
    Args:
        obj (Any): Object potentially containing numpy types
        
    Returns:
        Any: Object with numpy types converted to native Python types
    """
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj

def clean_and_convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and convert numeric columns in a DataFrame.
    
    This function attempts to convert columns to appropriate numeric types when possible
    and then to datetime types if conversion to numeric fails. This helps standardize
    DataFrame formats before analysis.
    
    Args:
        df (pd.DataFrame): DataFrame to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with appropriate data types
    """
    df = df.copy()  # Create a copy to avoid modifying the original DataFrame
    for col in df.columns:
        # Convert to numeric if possible
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Convert to datetime if possible and not already numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors='ignore')
            
    return df

def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert a pandas DataFrame to a list of dictionaries with proper type handling.
    
    This is often used to prepare DataFrame data for JSON serialization or
    for passing to an LLM. The function first converts the DataFrame to records
    (list of dicts) format, then ensures all numpy types are converted to native Python types.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert
        
    Returns:
        List[Dict[str, Any]]: List of row dictionaries with JSON-safe types
    """
    # First convert DataFrame to list of dictionaries
    records = df.to_dict(orient='records')
    
    # Now convert any numpy types
    return convert_numpy_types(records)

def prepare_data_for_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare data for inclusion in report by converting problematic types.
    
    This is a convenience wrapper around convert_numpy_types that's specifically
    meant for preparing data that will be included in the final report.
    
    Args:
        data (Dict[str, Any]): Data to prepare
        
    Returns:
        Dict[str, Any]: Prepared data safe for JSON serialization
    """
    return convert_numpy_types(data)
import json
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Union

class NumpyEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for numpy types.
    
    This encoder handles NumPy types that are not natively JSON serializable,
    including numpy.int64, numpy.float64, and numpy arrays. Without this custom
    encoder, JSON serialization will fail with "Object of type int64 is not JSON serializable".
    """
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        return super().default(obj)

def convert_numpy_types(obj: Any) -> Any:
    """
    Convert numpy types to native Python types.
    
    This is a recursive function that walks through nested data structures
    (dicts, lists) and converts any NumPy types to their native Python equivalents.
    This is essential when preparing data for JSON serialization or for sending
    to the LLM, which cannot handle NumPy types directly.
    
    Args:
        obj (Any): Object potentially containing numpy types
        
    Returns:
        Any: Object with numpy types converted to native Python types
    """
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj

def clean_and_convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and convert numeric columns in a DataFrame.
    
    This function attempts to convert columns to appropriate numeric types when possible
    and then to datetime types if conversion to numeric fails. This helps standardize
    DataFrame formats before analysis.
    
    Args:
        df (pd.DataFrame): DataFrame to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with appropriate data types
    """
    df = df.copy()  # Create a copy to avoid modifying the original DataFrame
    for col in df.columns:
        # Convert to numeric if possible
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Convert to datetime if possible and not already numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors='ignore')
            
    return df

def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert a pandas DataFrame to a list of dictionaries with proper type handling.
    
    This is often used to prepare DataFrame data for JSON serialization or
    for passing to an LLM. The function first converts the DataFrame to records
    (list of dicts) format, then ensures all numpy types are converted to native Python types.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert
        
    Returns:
        List[Dict[str, Any]]: List of row dictionaries with JSON-safe types
    """
    # First convert DataFrame to list of dictionaries
    records = df.to_dict(orient='records')
    
    # Now convert any numpy types
    return convert_numpy_types(records)

def prepare_data_for_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare data for inclusion in report by converting problematic types.
    
    This is a convenience wrapper around convert_numpy_types that's specifically
    meant for preparing data that will be included in the final report.
    
    Args:
        data (Dict[str, Any]): Data to prepare
        
    Returns:
        Dict[str, Any]: Prepared data safe for JSON serialization
    """
    return convert_numpy_types(data)
import json
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Union

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        return super().default(obj)

def convert_numpy_types(obj: Any) -> Any:
    """
    Convert numpy types to native Python types.
    
    Args:
        obj (Any): Object potentially containing numpy types
        
    Returns:
        Any: Object with numpy types converted to native Python types
    """
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj

def clean_and_convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and convert numeric columns in a DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = df.copy()
    for col in df.columns:
        # Convert to numeric if possible
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Convert to datetime if possible and not already numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors='ignore')
            
    return df

def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert a pandas DataFrame to a list of dictionaries with proper type handling.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert
        
    Returns:
        List[Dict[str, Any]]: List of row dictionaries
    """
    # First convert DataFrame to list of dictionaries
    records = df.to_dict(orient='records')
    
    # Now convert any numpy types
    return convert_numpy_types(records)

def prepare_data_for_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare data for inclusion in report by converting problematic types.
    
    Args:
        data (Dict[str, Any]): Data to prepare
        
    Returns:
        Dict[str, Any]: Prepared data safe for JSON serialization
    """
    return convert_numpy_types(data)
import numpy as np
import pandas as pd
from typing import Any, Dict, List
import json

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        return super().default(obj)

def convert_numpy_types(obj: Any) -> Any:
    """Convert numpy types to native Python types."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    return obj

def clean_and_convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and convert numeric columns in a DataFrame."""
    df = df.copy()
    for col in df.columns:
        # Convert to numeric if possible - use try-except instead of errors='ignore'
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            # Try to convert to datetime if numeric conversion failed
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                # If both conversions fail, leave as original type
                pass
    return df

def prepare_data_for_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare data for inclusion in report by converting problematic types."""
    return convert_numpy_types(data)
import numpy as np
import pandas as pd
from typing import Any, Dict, List

def convert_numpy_types(obj: Any) -> Any:
    """Convert numpy types to native Python types."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient='records')
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    return obj

def clean_and_convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and convert numeric columns in a DataFrame."""
    df = df.copy()
    for col in df.columns:
        # Convert to numeric if possible
        df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Convert to datetime if possible and not already numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors='ignore')
            
    return df

def prepare_data_for_report(data: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare data for inclusion in report by converting problematic types."""
    return convert_numpy_types(data)
import pandas as pd
import numpy as np
import json
from typing import Dict, Any, List, Union

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert a pandas DataFrame to a list of dictionaries.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert
        
    Returns:
        List[Dict[str, Any]]: List of row dictionaries
    """
    # Convert DataFrame to list of dictionaries
    records = df.to_dict(orient='records')
    
    # Serialize to JSON and back to ensure all values are JSON-compatible
    json_str = json.dumps(records, cls=NumpyEncoder)
    return json.loads(json_str)

def convert_dataframes(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert any pandas DataFrames in the data structure to lists of dictionaries.
    
    Args:
        data (Dict[str, Any]): Data structure that may contain DataFrames
        
    Returns:
        Dict[str, Any]: Converted data structure
    """
    if isinstance(data, pd.DataFrame):
        return dataframe_to_dict(data)
    elif isinstance(data, dict):
        return {k: convert_dataframes(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_dataframes(item) for item in data]
    else:
        return data

def clean_and_convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and convert numeric columns in a DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    for col in df.columns:
        # Convert to numeric if possible
        df[col] = pd.to_numeric(df[col], errors='ignore')
        
        # Convert to datetime if possible and not already numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors='ignore')
            
    return df

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
                df[col] = pd.to_numeric(df[col], errors='ignore')
                
            # Standardize date formats
            if col.lower().endswith('date'):
                df[col] = pd.to_datetime(df[col], errors='ignore')
        
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
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        return df.sort_values(by='date')

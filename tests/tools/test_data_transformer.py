import pytest
import pandas as pd
import numpy as np
import json
from datetime import datetime
from tools.data_transformer import (
    convert_numpy_types, clean_and_convert_numeric, 
    dataframe_to_dict, prepare_data_for_report,
    NumpyEncoder
)

class TestDataTransformer:
    """Tests for data transformer utilities."""
    
    def test_convert_numpy_types_primitives(self):
        """Test conversion of numpy primitive types."""
        # Setup test data
        test_data = {
            "int": np.int64(42),
            "float": np.float32(3.14),
            "bool": np.bool_(True),
            "array": np.array([1, 2, 3])
        }
        
        # Convert
        result = convert_numpy_types(test_data)
        
        # Assert
        assert type(result["int"]) == int
        assert type(result["float"]) == float
        assert type(result["bool"]) == bool
        assert type(result["array"]) == list
        assert result["int"] == 42
        assert abs(result["float"] - 3.14) < 0.01
        assert result["bool"] is True
        assert result["array"] == [1, 2, 3]
    
    def test_convert_numpy_types_nested(self):
        """Test conversion of nested structures with numpy types."""
        # Setup test data
        test_data = {
            "metrics": {
                "value": np.int64(100),
                "growth": np.float64(5.25)
            },
            "trends": [
                {"period": "2023", "value": np.int64(50)},
                {"period": "2022", "value": np.int64(40)}
            ]
        }
        
        # Convert
        result = convert_numpy_types(test_data)
        
        # Assert all values are converted
        assert type(result["metrics"]["value"]) == int
        assert type(result["metrics"]["growth"]) == float
        assert type(result["trends"][0]["value"]) == int
        assert type(result["trends"][1]["value"]) == int
    
    def test_convert_timestamp(self):
        """Test conversion of pandas Timestamp objects."""
        # Create a pandas Timestamp
        timestamp = pd.Timestamp("2023-12-31")
        data = {"date": timestamp}
        
        # Convert
        result = convert_numpy_types(data)
        
        # Should be converted to ISO format string
        assert isinstance(result["date"], str)
        assert result["date"] == "2023-12-31T00:00:00"
    
    def test_clean_and_convert_numeric(self):
        """Test cleaning and converting numeric data in DataFrames."""
        # Create a test DataFrame
        df = pd.DataFrame({
            "string_num": ["100", "200", "300"],
            "mixed": ["10", "not_a_number", "30"],
            "date_str": ["2023-12-31", "2023-01-01", "invalid_date"],
            "already_numeric": [1.1, 2.2, 3.3]
        })
        
        # Clean and convert
        result = clean_and_convert_numeric(df)
        
        # Assert
        assert pd.api.types.is_numeric_dtype(result["string_num"])
        assert result["string_num"].iloc[0] == 100
        
        # Mixed column should remain as object type
        assert not pd.api.types.is_numeric_dtype(result["mixed"])
        
        # Date column should be parsed where possible
        assert isinstance(result["date_str"].iloc[0], pd.Timestamp)
        assert isinstance(result["date_str"].iloc[1], pd.Timestamp)
        # Invalid date should be kept as is
        assert result["date_str"].iloc[2] == "invalid_date"
        
        # Already numeric column should remain numeric
        assert pd.api.types.is_numeric_dtype(result["already_numeric"])
    
    def test_numpy_encoder(self):
        """Test the custom NumpyEncoder for JSON serialization."""
        # Test data with numpy types
        test_data = {
            "int": np.int64(42),
            "float": np.float32(3.14),
            "array": np.array([1, 2, 3]),
            "timestamp": pd.Timestamp("2023-12-31")
        }
        
        # Serialize with our custom encoder
        json_str = json.dumps(test_data, cls=NumpyEncoder)
        
        # Parse back to Python
        result = json.loads(json_str)
        
        # Assert
        assert result["int"] == 42
        assert abs(result["float"] - 3.14) < 0.01
        assert result["array"] == [1, 2, 3]
        assert result["timestamp"] == "2023-12-31T00:00:00"
    
    def test_dataframe_to_dict(self):
        """Test converting DataFrame to dict with proper type handling."""
        # Create test DataFrame with complex types
        df = pd.DataFrame({
            "date": pd.date_range("2023-01-01", periods=3),
            "value": [np.int64(10), np.int64(20), np.int64(30)],
            "growth": [1.1, 2.2, np.nan]  # Include NaN to test handling
        })
        
        # Convert to dict
        result = dataframe_to_dict(df)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 3
        assert isinstance(result[0]["date"], str)
        assert isinstance(result[0]["value"], int)
        assert isinstance(result[0]["growth"], float)
        assert result[0]["value"] == 10
        assert result[2]["growth"] is None  # NaN should be converted to None

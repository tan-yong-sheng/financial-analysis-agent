# Data Transformer

The Data Transformer tool handles conversion between different data formats and ensures proper type handling, especially when working with Pandas DataFrames and NumPy arrays. It's a critical component for preventing JSON serialization errors when working with numerical data.

## Key Functions

### `convert_numpy_types(obj)`

This recursive function converts NumPy data types to native Python types, which is essential when:

- Serializing data to JSON
- Preparing data to send to the LLM
- Storing data in dictionaries that will later be serialized

**Example usage:**
```python
import numpy as np
from tools.data_transformer import convert_numpy_types

# Data with NumPy types
data = {
    "value": np.int64(42),
    "array": np.array([1, 2, 3]),
    "nested": {
        "float_value": np.float64(3.14)
    }
}

# Convert to Python native types
serializable_data = convert_numpy_types(data)
# Now safe to use with json.dumps()
```

### `clean_and_convert_numeric(df)`

This function cleans a Pandas DataFrame by attempting to convert columns to the appropriate data types:

1. First, it tries to convert columns to numeric types
2. For columns that can't be converted to numeric, it attempts to convert them to datetime
3. It returns a new DataFrame without modifying the original

**Example usage:**
```python
import pandas as pd
from tools.data_transformer import clean_and_convert_numeric

# DataFrame with mixed types
df = pd.DataFrame({
    'value': ['1', '2', '3'],
    'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'text': ['a', 'b', 'c']
})

# Clean and convert to appropriate types
cleaned_df = clean_and_convert_numeric(df)
# Now 'value' will be numeric and 'date' will be datetime
```

### `dataframe_to_dict(df)`

Converts a Pandas DataFrame to a list of dictionaries, ensuring all values are JSON-serializable:

1. Converts the DataFrame to records format (list of dictionaries)
2. Applies `convert_numpy_types` to handle any NumPy data types

**Example usage:**
```python
import pandas as pd
from tools.data_transformer import dataframe_to_dict

# Create a DataFrame
df = pd.DataFrame({
    'id': [1, 2, 3],
    'value': [10.5, 20.7, 30.2]
})

# Convert to list of dictionaries with serializable types
records = dataframe_to_dict(df)
```

## Custom JSON Encoder

### `NumpyEncoder`

A custom JSON encoder that handles NumPy types. Use this when you need to serialize objects containing NumPy types:

**Example usage:**
```python
import json
import numpy as np
from tools.data_transformer import NumpyEncoder

# Data with NumPy types
data = {
    "value": np.int64(42),
    "array": np.array([1, 2, 3])
}

# Serialize using custom encoder
json_str = json.dumps(data, cls=NumpyEncoder, indent=2)
```

## Common Issues

### JSON Serialization Errors

If you encounter a `TypeError: Object of type int64 is not JSON serializable` error, you need to use the Data Transformer:

```python
# Wrong approach - will cause error
json_str = json.dumps(data_with_numpy_types)

# Correct approach - Option 1
from tools.data_transformer import convert_numpy_types
safe_data = convert_numpy_types(data_with_numpy_types)
json_str = json.dumps(safe_data)

# Correct approach - Option 2
from tools.data_transformer import NumpyEncoder
json_str = json.dumps(data_with_numpy_types, cls=NumpyEncoder)
```

### Working with LLMs

When sending data from Pandas DataFrames or NumPy arrays to an LLM:

```python
from tools.data_transformer import convert_numpy_types

# Always convert data before including it in prompts
safe_data = convert_numpy_types(analysis_results)
prompt = f"""
Analyze this financial data:
{json.dumps(safe_data, indent=2)}
"""
```

## Best Practices

1. Always use `convert_numpy_types` before serializing data that might contain NumPy types
2. Use `clean_and_convert_numeric` when preparing DataFrames for analysis
3. Consider using the `NumpyEncoder` in your JSON dumps calls throughout the application
4. Be aware that Pandas operations often return NumPy types even if input data was native Python

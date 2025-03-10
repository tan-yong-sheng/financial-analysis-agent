# Tools Overview

Tools in the Financial Analysis System provide utility functions and services that support the agents and modules. They handle specific tasks such as data transformation, API communication, and web research.

## Available Tools

### [Data Transformer](data_transformer.md)

The Data Transformer tool manages data type conversion and provides utilities for handling NumPy and Pandas data types:

- Converts NumPy types to native Python types for JSON serialization
- Cleans and standardizes DataFrame content
- Provides a custom JSON encoder for handling complex data types
- Prevents common serialization errors when working with financial data

This tool is crucial for ensuring that data can be properly serialized when passing between agents or when saving results to files.

### [Financial Data Provider](financial_data_provider.md)

The Financial Data Provider tool handles communication with financial data APIs:

- Retrieves financial statements, metrics, and stock prices
- Manages API authentication and rate limiting
- Standardizes responses from data providers
- Handles errors and network issues gracefully

This tool serves as the interface between the system and external financial data sources.

### [Web Research Tool](web_research.md)

The Web Research Tool facilitates web-based research for gathering market information:

- Performs web searches using search APIs
- Collects news articles and industry information
- Filters and formats search results
- Manages API rate limits and authentication

This tool is primarily used by the Research Agent to gather non-financial information about companies and industries.

## Tool Design Principles

The tools in the system follow several key design principles:

1. **Single Responsibility**: Each tool focuses on a specific set of related functions
2. **Error Resilience**: Tools handle errors gracefully without crashing the overall system
3. **Configuration Flexibility**: Tools can be configured via environment variables or configuration files
4. **Consistent Interfaces**: Tools provide clear, consistent APIs for the rest of the system
5. **Reusability**: Tools are designed to be reusable across different parts of the system

## Adding New Tools

To add a new tool to the system:

1. Create a new Python file in the `tools` directory
2. Implement a class with appropriate methods for the tool's functionality
3. Add error handling and logging
4. Update the documentation
5. Import and use the tool in relevant agents or modules

## Tool Configuration

Tools can be configured through environment variables defined in the `.env` file or through the central `config.py` file. For example:

```python
# In config.py
FMP_BASE_URL = os.getenv('FMP_BASE_URL', "https://financialmodelingprep.com/api/v3")
MAX_SEARCH_RESULTS = 10

# In a tool implementation
from config import FMP_BASE_URL, MAX_SEARCH_RESULTS

class SomeTool:
    def __init__(self):
        self.base_url = FMP_BASE_URL
        self.max_results = MAX_SEARCH_RESULTS
```

## Example Usage

Here's how different tools might be used together:

```python
from tools.financial_data_provider import FinancialDataProvider
from tools.data_transformer import convert_numpy_types, NumpyEncoder
import json

# Get financial data
provider = FinancialDataProvider()
income_statement = provider.get_income_statement("AAPL")

# Convert NumPy types for serialization
safe_data = convert_numpy_types(income_statement)

# Serialize the data
json_data = json.dumps(safe_data, indent=2)

# Or use the custom encoder directly
json_data = json.dumps(income_statement, cls=NumpyEncoder, indent=2)
```

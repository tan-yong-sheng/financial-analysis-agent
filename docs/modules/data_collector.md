# Data Collector Module

The Data Collector module provides functionality for retrieving financial data from various sources, primarily through API calls to financial data providers. It serves as a standardized interface for gathering the raw data needed for analysis.

## Overview

The Data Collector simplifies the collection of financial information by providing clean methods to retrieve different types of financial data. It abstracts away the complexities of API calls, error handling, and data format standardization.

## Implementation

```python
class FinancialDataCollector:
    """Module for collecting and organizing financial data."""
    
    def __init__(self):
        """Initialize the financial data collector."""
        self.provider = FinancialDataProvider()
        
    def get_company_profile(self, ticker: str) -> List[Dict[str, Any]]:
        """Get company profile information."""
        # Implementation details...
    
    def get_income_statement(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """Get income statement data."""
        # Implementation details...
    
    # ...other methods for different financial data types...
    
    def get_comprehensive_data(self, ticker: str, period: str = "annual", limit: int = 5) -> Dict[str, Any]:
        """Get comprehensive financial data for a company."""
        # Implementation details...
```

## Key Data Collection Methods

### Company Profile

The `get_company_profile` method retrieves basic information about a company:

- Company name, ticker symbol, and description
- Industry and sector classification
- Current market capitalization and stock price
- Beta value and other key identifiers

Example output:
```json
[{
  "companyName": "Apple Inc.",
  "symbol": "AAPL",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "beta": 1.28,
  "price": 182.63,
  "mktCap": 2845000000000,
  "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers..."
}]
```

### Financial Statements

The module provides methods for retrieving the three main financial statements:

1. **Income Statement** (`get_income_statement`): Revenue, expenses, and profitability
2. **Balance Sheet** (`get_balance_sheet`): Assets, liabilities, and equity
3. **Cash Flow Statement** (`get_cash_flow`): Operating, investing, and financing cash flows

All statement methods accept parameters for:
- `period`: "annual" or "quarter" reporting periods
- `limit`: Number of historical periods to retrieve

### Additional Financial Data

The module also provides methods for retrieving:

- **Key Metrics** (`get_key_metrics`): Important financial metrics like EPS, ROE, etc.
- **Financial Ratios** (`get_financial_ratios`): Standard financial ratios for analysis
- **Stock Price** (`get_stock_price`): Historical and current stock price data
- **Technical Indicators** (`get_technical_indicators`): Technical analysis indicators
- **Analyst Estimates** (`get_analyst_estimates`): Forward-looking estimates

### Comprehensive Data Collection

The `get_comprehensive_data` method provides a convenient way to collect all relevant financial data for a company in a single call. It returns a dictionary containing:

```json
{
  "company_profile": [...],
  "income_statement": [...],
  "balance_sheet": [...],
  "cash_flow": [...],
  "key_metrics": [...],
  "financial_ratios": [...],
  "stock_price": {...},
  "analyst_estimates": [...]
}
```

## Error Handling

The Data Collector implements robust error handling:

1. API errors are caught and wrapped in a standardized format
2. Network issues are handled gracefully with appropriate error messages
3. Missing data is represented as empty lists rather than null values
4. Rate limiting and retry logic is implemented where appropriate

Example error handling:
```python
try:
    response = self.provider.get_income_statement(ticker, period, limit)
    return response
except Exception as e:
    logger.error(f"Error retrieving income statement for {ticker}: {str(e)}")
    return []
```

## Data Provider Integration

The Data Collector uses the FinancialDataProvider tool, which can be extended to support multiple data providers:

```python
# Default provider - Financial Modeling Prep
data = self.provider.get_income_statement(ticker, period, limit)

# With provider selection
data = self.alternative_provider.get_income_statement(ticker, period, limit)
```

## Example Usage

```python
from modules.data_collector import FinancialDataCollector

# Initialize the collector
collector = FinancialDataCollector()

# Get basic company information
profile = collector.get_company_profile("AAPL")
company_name = profile[0]["companyName"] if profile else "Unknown"
print(f"Analyzing: {company_name}")

# Get financial statements
income_data = collector.get_income_statement("AAPL", period="annual", limit=3)
balance_data = collector.get_balance_sheet("AAPL", period="annual", limit=3)
cash_flow_data = collector.get_cash_flow("AAPL", period="annual", limit=3)

# Get all data at once
all_data = collector.get_comprehensive_data("AAPL")

# Extract specific metrics
if income_data:
    latest_revenue = income_data[0]["revenue"]
    print(f"Latest Annual Revenue: ${latest_revenue:,}")
```

## Best Practices

When using the Data Collector module:

1. **Cache responses** when appropriate to reduce API calls
2. **Handle empty results** since not all companies have complete data
3. **Use appropriate periods** (annual for long-term analysis, quarterly for recent trends)
4. **Validate data** before analysis as formats can occasionally change
5. **Respect API rate limits** by throttling requests or implementing delays

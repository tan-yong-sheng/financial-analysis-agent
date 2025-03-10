# Financial Data Provider

The Financial Data Provider tool is responsible for communicating with financial data APIs to retrieve company financial information. It serves as the primary interface between the system and external financial data sources.

## Overview

The Financial Data Provider simplifies API interactions by providing a consistent interface for retrieving various types of financial data. It handles authentication, request formatting, error handling, and response processing.

## Implementation

```python
class FinancialDataProvider:
    """Provider for financial data from the Financial Modeling Prep API."""
    
    def __init__(self):
        """Initialize the financial data provider with API key."""
        self.api_key = FMP_API_KEY
        if not self.api_key:
            logger.warning("FMP_API_KEY not found in environment variables")
        self.base_url = FMP_BASE_URL
        
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the FMP API."""
        # Implementation details...
        
    # Methods for different financial data types
    def get_company_profile(self, ticker: str) -> List[Dict[str, Any]]:
        """Get company profile information."""
        # Implementation details...
    
    def get_income_statement(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """Get income statement data."""
        # Implementation details...
    
    # ...additional methods for other data types...
```

## Key API Methods

### API Request Handler

The `_make_request` method is the core of the Financial Data Provider, handling the actual HTTP requests:

```python
def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Make a request to the FMP API.
    
    Args:
        endpoint (str): API endpoint to call
        params (dict, optional): Query parameters
        
    Returns:
        dict: Response data
    """
    if params is None:
        params = {}
    
    # Add API key to parameters
    params['apikey'] = self.api_key
    
    url = f"{self.base_url}/{endpoint}"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error when calling {url}: {str(e)}")
        return {"error": str(e)}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error when calling {url}: {str(e)}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON response from {url}")
        return {"error": "Invalid JSON response"}
```

### Data Retrieval Methods

The provider includes methods for retrieving various types of financial data:

1. **Company Profile**: Basic information about a company (name, sector, description)
2. **Financial Statements**: Income statements, balance sheets, and cash flow statements
3. **Financial Metrics**: Key metrics, ratios, and indicators
4. **Stock Data**: Price data, technical indicators, and analyst estimates

Each method follows the same pattern:
1. Construct an API endpoint with the ticker symbol
2. Add any additional parameters (period, limit)
3. Make the API request
4. Return the structured response

## API Integration

The current implementation uses the [Financial Modeling Prep API](https://financialmodelingprep.com/developer/docs/) for financial data, but the provider is designed to be extensible for other data sources:

```python
# Current implementation with FMP
endpoint = f"income-statement/{ticker}"
params = {"period": period, "limit": limit}
return self._make_request(endpoint, params)

# Future implementation could add alternate providers
if self.provider == "alphavantage":
    endpoint = f"query"
    params = {"function": "INCOME_STATEMENT", "symbol": ticker, "apikey": self.api_key}
    return self._make_alternate_request(endpoint, params)
```

## Error Handling

The provider includes comprehensive error handling:

1. **HTTP Errors**: Status codes 4XX/5XX are caught and logged
2. **Network Errors**: Connection issues are handled gracefully
3. **JSON Parsing Errors**: Invalid responses are caught and reported
4. **API Key Validation**: Missing API keys generate warnings

All errors are logged with appropriate context information and returned as structured error objects:

```json
{"error": "HTTP Error 429: Too Many Requests - API rate limit exceeded"}
```

## Configuration

The Financial Data Provider is configured using environment variables and the `config.py` file:

```python
# In config.py
FMP_API_KEY = os.getenv('FMP_API_KEY')
FMP_BASE_URL = os.getenv('FMP_BASE_URL', "https://financialmodelingprep.com/api/v3")

# In provider implementation
self.api_key = FMP_API_KEY
self.base_url = FMP_BASE_URL
```

## Example Usage

```python
from tools.financial_data_provider import FinancialDataProvider

# Initialize the provider
provider = FinancialDataProvider()

# Get company profile
profile = provider.get_company_profile("AAPL")
if "error" not in profile:
    print(f"Company: {profile[0].get('companyName')}")
    print(f"Sector: {profile[0].get('sector')}")

# Get income statement
income_data = provider.get_income_statement("AAPL", period="annual", limit=3)
if "error" not in income_data and income_data:
    print(f"Latest Revenue: ${income_data[0].get('revenue'):,}")
    print(f"Latest Net Income: ${income_data[0].get('netIncome'):,}")
```

## Rate Limiting

The Financial Modeling Prep API has rate limits that vary by subscription level. The provider handles rate limit errors by returning them as structured error objects, but does not currently implement automatic retry logic or rate throttling.

Future enhancements could include:
- Implementing exponential backoff for retries
- Adding a request queue with rate limiting
- Caching responses to reduce duplicate API calls

## Alternative Data Providers

While the current implementation uses Financial Modeling Prep, the system could be extended to support other providers like:

- Alpha Vantage
- Yahoo Finance API
- Polygon.io
- Quandl

Adding a new provider would involve creating a new provider class or extending the existing one with alternative API endpoints and response formatting.

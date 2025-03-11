# Data Collection Agent

The Data Collection Agent is responsible for gathering financial data from various sources, primarily through financial APIs. It works with the Financial Data Provider tool to retrieve comprehensive financial information about companies with robust source tracking.

## Functionality

The Data Collection Agent:

1. Receives a ticker symbol and a research plan
2. Determines what specific data needs to be collected based on the plan
3. Retrieves financial statements, price data, technical indicators, and other metrics
4. Attaches source information to all retrieved data
5. Returns structured financial data for analysis with complete provenance information

## Implementation

The Data Collection Agent is implemented in the `DataCollectionAgent` class:

```python
class DataCollectionAgent(BaseAgent):
    """Agent responsible for collecting financial data."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial data collection specialist that gathers accurate financial information"
        super().__init__(role, "Data Collection", base_url=base_url, model_name=model_name)
        self.collector = FinancialDataCollector()
    
    def determine_data_needs(self, ticker: str, research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Determine what data needs to be collected based on the research plan."""
        # Implementation details...
    
    def collect_company_data(self, ticker: str, data_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data for a company based on the data collection plan."""
        # Implementation details...
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to collect financial information."""
        # Implementation details...
```

## Source Tracking

All data collected by this agent is enriched with source information using the `_source` field:

```python
result["_source"] = {
    "name": "Financial Modeling Prep API",
    "endpoint": f"profile/{ticker}",
    "date_retrieved": self._get_current_date(),
    "url": url.split('?')[0]  # Remove API key from URL
}
```

This source tracking enables:
- Proper attribution in final reports
- Data provenance verification
- Audit trails for compliance purposes
- Freshness assessment of financial information

## Input

The Data Collection Agent takes a JSON object containing:

```json
{
  "ticker": "AAPL",
  "research_plan": {
    "financial_analysis": {
      "income_statement": { "focus_areas": ["Revenue growth"] },
      "balance_sheet": { "focus_areas": ["Cash reserves"] }
    },
    "technical_analysis": {
      "indicators": ["SMA", "RSI"]
    }
  }
}
```

## Output

The Data Collection Agent produces structured financial data with source information:

```json
{
  "ticker": "AAPL",
  "company_profile": {
    "companyName": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "price": 182.63,
    "mktCap": 2845000000000,
    "beta": 1.28,
    "_source": {
      "name": "Financial Modeling Prep API",
      "endpoint": "profile/AAPL",
      "date_retrieved": "2023-05-15",
      "url": "https://financialmodelingprep.com/api/v3/profile/AAPL"
    }
  },
  "income_statement": [
    {
      "date": "2023-09-30",
      "revenue": 383946000000,
      "grossProfit": 170782000000,
      "netIncome": 96995000000,
      "_source": {
        "name": "Financial Modeling Prep API",
        "endpoint": "income-statement/AAPL",
        "period": "annual",
        "date_retrieved": "2023-05-15",
        "url": "https://financialmodelingprep.com/api/v3/income-statement/AAPL"
      }
    },
    // Additional periods...
  ],
  // Additional financial data...
}
```

## Key Methods

### `get_company_profile(ticker)`

Retrieves company profile information with source tracking:

```python
def get_company_profile(self, ticker: str) -> Dict[str, Any]:
    # API call implementation...
    
    # Add source information to data
    result["_source"] = {
        "name": "Financial Modeling Prep API",
        "endpoint": f"profile/{ticker}",
        "date_retrieved": self._get_current_date(),
        "url": url.split('?')[0]
    }
        
    return result
```

### `determine_data_needs(ticker, research_plan)`

Uses LLM to analyze the research plan and determine what specific data needs to be collected.

### `collect_company_data(ticker, data_plan)`

Collects all required data according to the data plan, with source information attached to each data component.

### `get_technical_indicators(ticker, indicator_name, time_period)`

Retrieves technical indicators with proper source attribution:

```python
def get_technical_indicators(self, ticker: str, indicator_name: str = None, time_period: int = 14) -> Dict[str, Any]:
    # Implementation details...
    
    # Add source information
    source_info = {
        "name": "Financial Modeling Prep API",
        "endpoint": f"technical_indicator/daily/{ticker}",
        "indicator": indicator_name,
        "period": time_period,
        "date_retrieved": self._get_current_date(),
        "url": url.split('?')[0]
    }
```

## Data Sources

The Data Collection Agent primarily uses the Financial Modeling Prep API through the Financial Data Provider tool. Alternative data sources can be added by extending the Financial Data Provider.

## Error Handling

The agent handles various data collection errors:

1. Missing or invalid ticker symbols
2. API rate limits or connectivity issues
3. Incomplete or missing financial statements
4. Timeouts during data retrieval

## Observability

Data collection operations are logged with:
- Source endpoint information
- Result summaries
- Timestamps
- Error conditions

## Example Usage

```python
from agents.data_collection_agent import DataCollectionAgent

# Initialize the agent
collector = DataCollectionAgent()

# Create input data
input_data = {
    "ticker": "AAPL",
    "research_plan": {
        "financial_analysis": {
            "income_statement": { "focus_areas": ["Revenue growth"] }
        }
    }
}

# Collect the financial data
financial_data = collector.process(input_data)

# Access specific data with source information
income_statement = financial_data.get("income_statement", [])
print(f"Latest revenue: ${income_statement[0]['revenue'] / 1000000000:.2f} billion")
print(f"Source: {income_statement[0]['_source']['name']}, Retrieved: {income_statement[0]['_source']['date_retrieved']}")
```

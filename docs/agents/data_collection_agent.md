# Data Collection Agent

The Data Collection Agent is responsible for gathering financial data from various sources, primarily through financial APIs. It works with the Financial Data Provider tool to retrieve comprehensive financial information about companies.

## Functionality

The Data Collection Agent:

1. Receives a ticker symbol and a research plan
2. Determines what specific data needs to be collected based on the plan
3. Retrieves financial statements, price data, technical indicators, and other metrics
4. Returns structured financial data for analysis

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

The Data Collection Agent produces structured financial data:

```json
{
  "ticker": "AAPL",
  "company_profile": [{
    "companyName": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "price": 182.63,
    "mktCap": 2845000000000,
    "beta": 1.28
  }],
  "income_statement": [
    {
      "date": "2023-09-30",
      "revenue": 383946000000,
      "grossProfit": 170782000000,
      "netIncome": 96995000000
    },
    {
      "date": "2022-09-30",
      "revenue": 394328000000,
      "grossProfit": 170782000000,
      "netIncome": 99803000000
    }
  ],
  "balance_sheet": [
    {
      "date": "2023-09-30",
      "totalAssets": 352583000000,
      "totalLiabilities": 290448000000,
      "totalStockholdersEquity": 62135000000,
      "cashAndCashEquivalents": 29965000000
    }
  ],
  "technical_indicators": {
    "sma": {
      "historical": [
        {
          "date": "2023-12-15",
          "sma": 187.32
        }
      ]
    },
    "rsi": {
      "historical": [
        {
          "date": "2023-12-15",
          "rsi": 54.78
        }
      ]
    }
  }
}
```

## Key Methods

### `determine_data_needs(ticker, research_plan)`

Uses LLM to analyze the research plan and determine what specific data needs to be collected:

1. Identifies which financial statements are needed
2. Determines what period and limit settings to use
3. Lists technical indicators to calculate
4. Specifies ratios and metrics that should be collected
5. Identifies any competitor tickers that should also be analyzed

### `collect_company_data(ticker, data_plan)`

Executes the data collection plan by:

1. Retrieving company profile information
2. Collecting required financial statements (income statement, balance sheet, cash flow)
3. Getting key metrics and financial ratios
4. Calculating technical indicators
5. Retrieving analyst estimates and stock price data
6. Optionally collecting data for competitor companies

### `process(input_data)`

The main entry point that:

1. Validates the input data
2. Extracts the ticker symbol and research plan
3. Determines the data collection needs
4. Executes the data collection
5. Returns the comprehensive financial data

## Data Sources

The Data Collection Agent primarily uses the Financial Modeling Prep API through the Financial Data Provider tool. Alternative data sources can be added by extending the Financial Data Provider.

## Error Handling

The agent handles various data collection errors:

1. Missing or invalid ticker symbols
2. API rate limits or connectivity issues
3. Incomplete or missing financial statements
4. Timeouts during data retrieval

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

# Access specific data
income_statement = financial_data.get("income_statement", [])
print(f"Latest revenue: ${income_statement[0]['revenue'] / 1000000000:.2f} billion")
```

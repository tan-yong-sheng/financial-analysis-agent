# Data Providers

## Financial Modeling Prep API

The system primarily uses Financial Modeling Prep (FMP) API for financial data:

### Available Data
- Income Statements
- Balance Sheets
- Cash Flow Statements
- Company Profiles
- Stock Prices
- Technical Indicators
- Financial Ratios
- Analyst Estimates

### Configuration

```python
FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
```

## Google Search API (via Serper)

Used for web research and news gathering:

### Features
- Web Search
- News Search
- Content Filtering
- Result Processing

### Configuration

```python
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
MAX_SEARCH_RESULTS = 5
```

## Adding New Data Providers

To add a new data provider:

1. Create a new provider class in `tools/`
2. Implement required methods
3. Update configuration
4. Integrate with Data Collection Agent

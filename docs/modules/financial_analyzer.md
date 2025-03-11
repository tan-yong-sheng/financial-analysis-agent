# Financial Analyzer Module

The Financial Analyzer module provides comprehensive analysis of financial data through algorithms and computational techniques. This module calculates key financial metrics, identifies trends, and generates quantitative insights without using LLM capabilities.

## Overview

The Financial Analyzer takes raw financial data (income statements, balance sheets, cash flow statements, etc.) and performs various analyses to extract meaningful quantitative insights. It serves as the computational engine behind the Analysis Agent's financial assessments.

## Implementation

```python
class FinancialAnalyzer:
    """Module for analyzing financial data."""
    
    def __init__(self):
        """Initialize the financial analyzer."""
        pass
        
    def analyze_income_statement(self, income_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze income statement data."""
        # Implementation details...
            
    def analyze_balance_sheet(self, balance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze balance sheet data."""
        # Implementation details...
            
    def analyze_cash_flow(self, cash_flow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cash flow statement data."""
        # Implementation details...
            
    def analyze_technical_data(self, technical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical indicators data."""
        # Implementation details...
    
    def comprehensive_analysis(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive analysis of financial data."""
        # Implementation details...
```

## Key Analysis Functions

### Income Statement Analysis

The `analyze_income_statement` method calculates:

- Revenue growth rates year-over-year
- Net income growth rates
- Gross, operating, and profit margins
- Expense ratios and their trends

Example output:
```json
{
  "summary": {
    "latest_year": "2023-09-30",
    "latest_revenue": 383946000000,
    "latest_net_income": 96995000000
  },
  "growth": {
    "revenue_growth": 2.02,
    "net_income_growth": -3.36
  },
  "margins": {
    "gross_margin": 46.21,
    "operating_margin": 31.51,
    "profit_margin": 24.79
  },
  "trends": [...]
}
```

### Balance Sheet Analysis

The `analyze_balance_sheet` method calculates:

- Liquidity ratios (current ratio, quick ratio)
- Solvency metrics (debt-to-equity, debt-to-assets)
- Asset turnover and efficiency metrics
- Working capital analysis

Example output:
```json
{
  "summary": {
    "latest_date": "2023-09-30",
    "total_assets": 352583000000,
    "total_liabilities": 290448000000,
    "stockholders_equity": 62135000000
  },
  "ratios": {
    "current_ratio": 0.89,
    "debt_to_assets": 0.82,
    "return_on_assets": 0.18
  },
  "trends": [...]
}
```

### Cash Flow Analysis

The `analyze_cash_flow` method calculates:

- Free cash flow and its trends
- Operating cash flow analysis
- Cash flow to income ratios
- Capital expenditure analysis
- Cash generation efficiency

Example output:
```json
{
  "summary": {
    "latest_date": "2023-09-30",
    "operating_cash_flow": 118283000000,
    "investing_cash_flow": -22645000000,
    "financing_cash_flow": -95028000000
  },
  "metrics": {
    "free_cash_flow": 109083000000,
    "capital_expenditure": 9200000000
  },
  "trends": [...]
}
```

### Technical Indicator Analysis

The `analyze_technical_data` method processes various technical indicators:

- Moving averages (SMA, EMA)
- Relative Strength Index (RSI)
- Analysis of recent trends and signals

Example output:
```json
{
  "sma": {
    "latest_value": 187.32,
    "average_value": 183.47,
    "recent_trend": "up",
    "recent_values": [...]
  },
  "rsi": {
    "latest_value": 54.78,
    "average_value": 51.23,
    "recent_trend": "down",
    "recent_values": [...]
  }
}
```

### Comprehensive Analysis

The `comprehensive_analysis` method combines all individual analyses:

1. Analyzes income statement, balance sheet, and cash flow statement
2. Processes technical indicators if available
3. Creates a comprehensive summary of the company's financial health
4. Returns a structured analysis result with all metrics organized logically

## Data Handling

The Financial Analyzer uses several techniques to ensure robust data handling:

- **NumPy Type Handling**: Special handling for NumPy data types when analyzing Pandas DataFrames
- **Missing Data Protection**: Checks for missing or `null` values before calculations
- **Exception Handling**: Each analysis method catches and reports exceptions without halting the entire analysis
- **Clean DataFrames**: Uses `clean_and_convert_numeric` from Data Transformer to standardize data types

## Key Calculations

### Growth Metrics

```python
# Year-over-year revenue growth
df['revenue_growth'] = df['revenue'].pct_change(-1) * 100
```

### Margin Calculations

```python
# Gross margin calculation
if 'grossProfit' in df.columns and 'revenue' in df.columns:
    df['gross_margin'] = (df['grossProfit'] / df['revenue']) * 100
```

### Ratio Calculations

```python
# Current ratio calculation
if 'totalCurrentAssets' in df.columns and 'totalCurrentLiabilities' in df.columns:
    df['current_ratio'] = df['totalCurrentAssets'] / df['totalCurrentLiabilities']
```

### Free Cash Flow

```python
# Free cash flow calculation
if 'netCashProvidedByOperatingActivities' in df.columns and 'capitalExpenditure' in df.columns:
    df['free_cash_flow'] = df['netCashProvidedByOperatingActivities'] - df['capitalExpenditure']
```

## Example Usage

```python
from modules.financial_analyzer import FinancialAnalyzer

# Initialize the analyzer
analyzer = FinancialAnalyzer()

# Analyze an income statement
income_analysis = analyzer.analyze_income_statement(income_statement_data)
print(f"Revenue growth: {income_analysis['growth']['revenue_growth']}%")
print(f"Profit margin: {income_analysis['margins']['profit_margin']}%")

# Perform comprehensive analysis
results = analyzer.comprehensive_analysis(all_financial_data)
```

## Error Handling

The Financial Analyzer implements robust error handling:

1. Each analysis method is wrapped in try-except blocks
2. Errors are logged with detailed information
3. Partial results are returned when possible instead of failing entirely
4. Error messages are included in the output for troubleshooting

Example error handling:
```python
try:
    # Analysis calculations
    # ...
except Exception as e:
    logger.error(f"Error analyzing income statement: {str(e)}")
    return {"error": f"Analysis failed: {str(e)}"}
```

## Integration with Other Components

The Financial Analyzer is primarily used by:

1. **Analysis Agent**: For computational analysis of financial data
2. **Fact Check Agent**: For validating numerical claims in reports

However, it's designed to be usable independently from the agent system for standalone financial analysis tasks.

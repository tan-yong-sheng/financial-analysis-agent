# Usage Guide

This guide provides detailed instructions on how to use the Financial Analysis System for different scenarios.

## Basic Usage

### Generating a Standard Financial Report

To generate a standard financial report for a company, use the main script with a ticker symbol:

```bash
python main.py --ticker AAPL
```

The system will:

1. Generate a research plan for the company
2. Collect financial data based on the plan
3. Research the company's industry and competitors
4. Analyze the financial data
5. Create a comprehensive report
6. Save the report to the `reports` directory

### Customizing Report Output Location

You can specify a custom output location for the reports:

```bash
python main.py --ticker MSFT --output /path/to/custom/directory
```

## Working with the Generated Reports

### Report Format

The system generates two output files:

1. **Markdown Report** (`TICKER_analysis.md`): A human-readable report with financial analysis
2. **JSON Results** (`TICKER_results.json`): Structured data containing all analysis results

The Markdown report can be:
- Converted to PDF or other formats using tools like Pandoc
- Published on websites or wikis
- Shared with stakeholders directly

The JSON results can be:
- Used for further programmatic analysis
- Imported into dashboards
- Used to compare multiple companies

### Converting to PDF

To convert the Markdown report to a PDF, install Pandoc and use:

```bash
pandoc reports/AAPL_analysis.md -o reports/AAPL_analysis.pdf
```

## Advanced Usage

### Accessing Individual Components

You can use the individual components of the system in your own code:

```python
from orchestrator import FinancialAnalysisOrchestrator

# Initialize the orchestrator
orchestrator = FinancialAnalysisOrchestrator()

# Analyze a company
results = orchestrator.analyze_company("AAPL")

# Access different parts of the results
company_profile = results["company_profile"]
financial_data = results["financial_data"]
analysis = results["analysis_results"]
report = results["report"]

# Do something with the components
print(f"Company: {company_profile[0]['companyName']}")
print(f"Current Price: ${company_profile[0]['price']}")
```

### Using the Financial Data Collector

You can use the Financial Data Collector directly:

```python
from modules.data_collector import FinancialDataCollector

# Initialize the collector
collector = FinancialDataCollector()

# Get specific data
income_statement = collector.get_income_statement("AAPL", period="annual", limit=5)
balance_sheet = collector.get_balance_sheet("AAPL", period="annual", limit=5)
cash_flow = collector.get_cash_flow("AAPL", period="annual", limit=5)

# Get comprehensive data
all_data = collector.get_comprehensive_data("AAPL", period="annual", limit=5)
```

### Using the Financial Analyzer

You can use the Financial Analyzer independently:

```python
from modules.financial_analyzer import FinancialAnalyzer

# Initialize the analyzer
analyzer = FinancialAnalyzer()

# Analyze financial data
analysis = analyzer.comprehensive_analysis(financial_data)

# Access specific analyses
income_analysis = analysis["income_analysis"]
balance_sheet_analysis = analysis["balance_sheet_analysis"]
cash_flow_analysis = analysis["cash_flow_analysis"]
```

## Integrating with Other Systems

### API Integration

While the system doesn't include a built-in API, you can integrate it with an API framework like Flask or FastAPI:

```python
from flask import Flask, request, jsonify
from orchestrator import FinancialAnalysisOrchestrator

app = Flask(__name__)
orchestrator = FinancialAnalysisOrchestrator()

@app.route('/analyze/<ticker>', methods=['GET'])
def analyze_company(ticker):
    results = orchestrator.analyze_company(ticker)
    return jsonify({
        'ticker': ticker,
        'company_name': results['company_profile'][0]['companyName'],
        'report': results['report']
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Batch Processing

For analyzing multiple companies:

```python
from orchestrator import FinancialAnalysisOrchestrator
import os

# Initialize the orchestrator
orchestrator = FinancialAnalysisOrchestrator()

# List of tickers to analyze
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

# Output directory
output_dir = "batch_reports"
os.makedirs(output_dir, exist_ok=True)

# Process each ticker
for ticker in tickers:
    print(f"Analyzing {ticker}...")
    try:
        results = orchestrator.analyze_company(ticker)
        print(f"Completed {ticker}")
    except Exception as e:
        print(f"Error analyzing {ticker}: {str(e)}")
```

## Performance Considerations

- Analysis for a single company typically takes 1-5 minutes depending on complexity
- Web research is the most time-consuming step and depends on internet connectivity
- LLM calls can sometimes timeout; retry mechanisms are built into the system
- JSON serialization of large datasets can be memory-intensive

## Common Patterns and Best Practices

1. **API Key Security**: Never commit your `.env` file to version control
2. **Error Handling**: Always check for the `error` key in returned results
3. **Data Validation**: Verify financial data is available before proceeding with analysis
4. **Report Post-processing**: Consider additional formatting or style improvements to reports
5. **Memory Management**: For batch processing, consider implementing garbage collection

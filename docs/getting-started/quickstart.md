# Quick Start Guide

This guide will help you run your first financial analysis using the Financial Analysis Agent system.

## Prerequisites

- Completed [installation](installation.md) and [configuration](configuration.md)
- Valid API keys in your `.env` file

## Basic Usage

### Command Line Interface

The simplest way to run an analysis is through the command line:

```bash
python run.py --ticker AAPL
```

This will:
1. Collect financial data for Apple Inc.
2. Conduct market research
3. Analyze the data
4. Generate a comprehensive report

### Output

The analysis will generate:

- A markdown report in `reports/AAPL_analysis.md`
- Raw analysis results in `reports/AAPL_results.json`

## Python API Usage

You can also use the system programmatically:

```python
from orchestrator import FinancialAnalysisOrchestrator

# Initialize the orchestrator
orchestrator = FinancialAnalysisOrchestrator()

# Run analysis for a company
result = orchestrator.analyze_company("MSFT")

# Check for errors
if "error" in result:
    print(f"Analysis failed: {result['error']}")
else:
    print(f"Analysis completed in {result['execution_time']:.2f} seconds")
    print(f"Report saved to: {result['report_path']}")
```

## Advanced Options

### Custom Analysis Parameters

```bash
python run.py --ticker AAPL --period quarterly --limit 8 --depth full
```

### Compare Multiple Companies

```bash
python run.py --tickers AAPL,MSFT,GOOG --mode compare
```

### Focus on Specific Analysis Areas

```bash
python run.py --ticker AMZN --focus "cash flow,profitability,growth trends"
```

## Example Output

Here's a snippet of what the analysis report looks like:

```markdown
# Financial Analysis: Apple Inc. (AAPL)

## Executive Summary

Apple Inc. demonstrates strong financial performance with stable revenue growth of 2.0% year-over-year and industry-leading profit margins of 24.8%. The company maintains a robust balance sheet with substantial cash reserves of $162.1 billion and low debt-to-equity ratio of 1.23.

Key insights:
- Services revenue continues to grow at 9.1%, outpacing hardware segments [Source: FMP API, 2023-09-30]
- Strong position in premium smartphone market with 42% share [Source: MarketWatch, 2023-08-10]
- Potential challenges from emerging AI competitors in consumer electronics
```

## Next Steps

- Explore the [detailed documentation](../agents/overview.md) for each agent
- Learn how to [customize the analysis process](../guides/customization.md)
- Check out [example analyses](../examples/basic-usage.md)

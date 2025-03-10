# Modules Overview

Modules in the Financial Analysis System provide core functionality for data processing and analysis without the LLM-powered reasoning of agents. They serve as the computational backbone of the system, implementing algorithms for financial analysis and data handling.

## Key Differences Between Modules and Agents

| Modules | Agents |
|---------|--------|
| Focus on computation and data processing | Focus on reasoning and decision-making |
| Do not use LLM capabilities directly | Leverage LLMs for complex tasks |
| Deterministic output for a given input | May vary in output based on LLM responses |
| Reusable across different workloads | Specialized for specific parts of the workflow |

## Available Modules

### [Financial Analyzer](financial_analyzer.md)

The Financial Analyzer module performs quantitative analysis of financial data:

- Calculates financial ratios and metrics
- Analyzes income statements, balance sheets, and cash flows
- Identifies trends in financial performance
- Evaluates technical indicators

This module provides pure computational analysis without qualitative interpretation, which is later added by the Analysis Agent.

### [Data Collector](data_collector.md)

The Data Collector module interfaces with financial data sources to retrieve raw data:

- Fetches financial statements from APIs
- Retrieves stock price and technical indicator data
- Collects company profile information
- Standardizes data formats for further processing

This module abstracts away the complexities of data retrieval, allowing other components to work with clean, standardized data.

## Module Architecture

Modules are implemented as Python classes with a focus on:

1. **Clean interfaces**: Well-defined input and output structures
2. **Error handling**: Robust handling of API failures and data issues
3. **Data transformation**: Converting between different formats and handling special types
4. **Performance optimization**: Efficient processing of financial data

## Using Modules Independently

Modules can be used independently of the agent system for focused tasks:

```python
from modules.data_collector import FinancialDataCollector
from modules.financial_analyzer import FinancialAnalyzer

# Initialize modules
collector = FinancialDataCollector()
analyzer = FinancialAnalyzer()

# Collect data
financial_data = collector.get_comprehensive_data("AAPL")

# Analyze data
analysis_results = analyzer.comprehensive_analysis(financial_data)

# Use specific analysis functions
income_analysis = analyzer.analyze_income_statement(financial_data["income_statement"])
```

## Extending the Module System

To add a new module to the system:

1. Create a new Python class in the `modules` directory
2. Implement the necessary functionality with clear method interfaces
3. Add proper error handling and logging
4. Update documentation for the new module
5. Integrate with existing modules or agents as needed

## Best Practices

When working with modules:

1. **Separate concerns**: Keep data collection separate from analysis
2. **Handle edge cases**: Account for missing or incomplete data
3. **Document interfaces**: Clearly document input and output formats
4. **Use type hints**: Leverage Python type hints for better code clarity
5. **Write unit tests**: Test modules independently from agents

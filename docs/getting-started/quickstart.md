# Quick Start Guide

This guide will help you get up and running with the Financial Analysis Agent System quickly.

## Basic Usage

1. Run a simple analysis:
```bash
python main.py --ticker AAPL
```

2. The system will generate:
   - A comprehensive financial analysis report
   - Interactive stock charts
   - Analysis results in JSON format

## Example Output

```python
from orchestrator import FinancialAnalysisOrchestrator

# Initialize orchestrator
orchestrator = FinancialAnalysisOrchestrator()

# Analyze a company
results = orchestrator.analyze_company("AAPL")

# Access results
print(f"Report saved to: {results['report_path']}")
print(f"Analysis completed in: {results['execution_time']:.2f} seconds")
```

## Next Steps

- Learn about [advanced configuration options](configuration.md)
- Explore the [agent system architecture](../components/agent-system.md)
- Check out [example analyses](../examples/basic-usage.md)

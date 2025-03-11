# Customization Guide

This guide explains how to customize the Financial Analysis Agent for your specific needs.

## Configuration Options

### Custom Analysis Parameters

```python
from config import AnalysisConfig

config = AnalysisConfig(
    period="quarterly",
    limit=8,
    technical_indicators=["RSI", "MACD", "SMA"],
    depth="full"
)
```

### Custom Data Sources

1. Create a new data provider:
```python
from tools.financial_data_provider import BaseDataProvider

class CustomDataProvider(BaseDataProvider):
    def get_financial_data(self, ticker: str):
        # Implementation
```

2. Register the provider:
```python
from orchestrator import FinancialAnalysisOrchestrator

orchestrator = FinancialAnalysisOrchestrator()
orchestrator.register_data_provider(CustomDataProvider())
```

## Custom Analysis Rules

Create custom analysis rules in `config/analysis_rules.json`:

```json
{
  "financial_ratios": {
    "current_ratio": {
      "warning_threshold": 1.5,
      "critical_threshold": 1.0
    }
  }
}
```

## Report Templates

Customize report templates in `templates/`:

```markdown
# {{company_name}} ({{ticker}}) Analysis Report

## Executive Summary
{{summary}}

## Financial Analysis
{{financial_analysis}}
```

## Advanced Customization

See the [API Reference](../api-reference.md) for more customization options.

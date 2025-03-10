# Basic Usage Examples

## Simple Analysis

The simplest way to analyze a company is using the command line:

```bash
python main.py --ticker AAPL
```

## Programmatic Usage

```python
from orchestrator import FinancialAnalysisOrchestrator

# Initialize the orchestrator
orchestrator = FinancialAnalysisOrchestrator()

# Analyze a company
results = orchestrator.analyze_company("AAPL")

# Access various components of the results
print(f"Report saved to: {results['report_path']}")
print(f"Analysis time: {results['execution_time']:.2f} seconds")

# Access financial data
financial_data = results['financial_data']
analysis = results['analysis_results']
research = results['research_results']
```

## Custom Analysis

You can also use individual components:

```python
from agents import PlannerAgent, DataCollectionAgent, AnalysisAgent
from tools import ChartGenerator

# Create agents
planner = PlannerAgent()
collector = DataCollectionAgent()
analyst = AnalysisAgent()

# Create a research plan
plan = planner.process({"ticker": "AAPL"})

# Collect data
data = collector.process({
    "ticker": "AAPL",
    "research_plan": plan
})

# Analyze data
analysis = analyst.process({
    "financial_data": data,
    "research_plan": plan
})

# Generate charts
chart_gen = ChartGenerator()
chart_path = chart_gen.create_candlestick_chart(
    data["stock_price"],
    "AAPL"
)
```

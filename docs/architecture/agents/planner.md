# Planner Agent

The Planner Agent is responsible for creating comprehensive research plans and structuring the analysis approach.

## Responsibilities

- Creating detailed research plans
- Identifying key financial metrics to analyze
- Determining technical indicators to track
- Planning competitive analysis scope
- Structuring the final report format

## Implementation

```python
from agents.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self):
        role = "a strategic financial research planner"
        super().__init__(role, "Research Planner")
```

## Key Methods

### create_research_plan
Creates a structured research plan based on company information:
- Financial analysis requirements
- Technical analysis scope
- Industry research needs
- Recent developments to track
- Report structure

### process
Main entry point that processes input data and creates the research plan.

## Example Usage

```python
planner = PlannerAgent()
research_plan = planner.process({
    "ticker": "AAPL",
    "company_info": company_info
})
```

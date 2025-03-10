# Agents API Reference

## BaseAgent

The base class for all specialized agents.

```python
from agents.base_agent import BaseAgent

class BaseAgent:
    def __init__(self, role: str, agent_name: str)
    def _call_llm(self, prompt: str, temperature: Optional[float] = None) -> str
    def process(self, input_data: Any) -> Any
    def reset_memory(self)
```

## PlannerAgent

```python
from agents.planner_agent import PlannerAgent

agent = PlannerAgent()
plan = agent.process({
    "ticker": "AAPL",
    "company_info": {...}
})
```

## DataCollectionAgent

```python
from agents.data_collection_agent import DataCollectionAgent

agent = DataCollectionAgent()
data = agent.process({
    "ticker": "AAPL",
    "research_plan": {...}
})
```

[View full agents documentation →](../components/agent-system.md)

# Agent System

The Agent System is the core architecture of the Financial Analysis Agent, providing the framework for specialized agents to work together.

## Architecture Overview

The agent system follows a modular design where each agent has specific responsibilities:

```
           ┌─────────────────┐
           │                 │
           │   Orchestrator  │
           │                 │
           └────────┬────────┘
                    │
      ┌─────────────┼─────────────┐
      │             │             │
┌─────▼───┐   ┌─────▼───┐   ┌─────▼───┐
│         │   │         │   │         │
│ Agent 1 │   │ Agent 2 │   │ Agent 3 │
│         │   │         │   │         │
└─────────┘   └─────────┘   └─────────┘
```

## BaseAgent Implementation

All agents inherit from the `BaseAgent` class:

```python
class BaseAgent:
    def __init__(self, role: str, name: str):
        self.role = role
        self.name = name
        
    def _call_llm(self, prompt: str) -> str:
        """Call LLM with prompt and return response."""
        
    def _call_structured_llm(self, prompt: str, response_model: Type[T]) -> T:
        """Call LLM with prompt and return structured response."""
        
    def process(self, input_data: Any) -> Any:
        """Process input data according to agent's role."""
```

## Agent Communication

Agents communicate through structured data exchanges:

1. Each agent takes input data in a standardized format
2. Each agent returns output data in a standardized format
3. The orchestrator ensures data compatibility between agents

## Agent Types

The system includes the following agent types:

- **Data Collection Agent**: Gathers financial data
- **Research Agent**: Conducts market research
- **Analysis Agent**: Analyzes financial data
- **Report Agent**: Generates reports
- **Fact Check Agent**: Validates report accuracy

## Extending the Agent System

To create a new agent type:

1. Inherit from the `BaseAgent` class
2. Define specialized methods for the agent's role
3. Implement the `process` method to handle input and produce output

Example:

```python
class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("custom role description", "Custom Agent")
        
    def specialized_method(self):
        # Custom functionality...
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Process logic...
        return result
```

## Agent System Benefits

- **Modularity**: Each agent has a single responsibility
- **Testability**: Agents can be tested in isolation
- **Maintainability**: Changes to one agent don't affect others
- **Flexibility**: Agents can be swapped or modified independently

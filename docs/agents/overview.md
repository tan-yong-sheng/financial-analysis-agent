# Agent System Overview

The Financial Analysis Agent uses a multi-agent architecture where specialized agents handle different aspects of the financial analysis workflow.

## Agent Architecture

The system divides responsibilities among specialized agents that work together:

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │     │                   │
│  Data Collection  │────▶│     Research      │────▶│     Analysis      │
│      Agent        │     │      Agent        │     │      Agent        │
│                   │     │                   │     │                   │
└───────────────────┘     └───────────────────┘     └───────────────────┘
                                                            │
                                                            ▼
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │     │                   │
│   Fact Check      │◀────│      Report       │◀────│    Orchestrator   │
│      Agent        │     │      Agent        │     │                   │
│                   │     │                   │     │                   │
└───────────────────┘     └───────────────────┘     └───────────────────┘
```

## Core Agents

### [Data Collection Agent](data_collection_agent.md)
Retrieves financial data from various sources and attaches source information to all data.

### [Research Agent](research_agent.md)
Conducts market research, gathering information from web sources with proper citation tracking.

### [Analysis Agent](analysis_agent.md)
Analyzes financial data and research findings to generate insights while preserving citations.

### [Report Agent](report_agent.md)
Generates comprehensive reports from analysis results, maintaining citations for transparency.

### [Fact Check Agent](fact_check_agent.md)
Verifies facts and citations in the final report to ensure accuracy and completeness.

## Agent Interaction

Agents coordinate through the Orchestrator which:

1. Manages the workflow between agents
2. Passes data and results between agents
3. Ensures source information and citations are preserved throughout

## BaseAgent Class

All agents inherit from the `BaseAgent` class which provides:

- Standard LLM interaction methods
- Structured output capabilities
- Memory management 
- Error handling
- Observability and logging

## Agent System Benefits

- **Specialization**: Each agent focuses on its specific domain
- **Composability**: Agents can be used individually or as part of the workflow
- **Traceability**: Information flows are clear and attributable
- **Extensibility**: New agent types can be added to extend system capabilities

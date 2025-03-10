# Agents Overview

The Financial Analysis System uses a multi-agent architecture where specialized agents work together to produce comprehensive financial analysis reports. Each agent is designed to handle a specific part of the workflow, allowing for modular design and focused expertise.

## Agent Architecture

All agents in the system inherit from the `BaseAgent` class, which provides common functionality:

- Communication with the LLM
- Conversation memory management
- Standard input/output formats
- Error handling

## Agent Types

The system includes the following specialized agents:

### [Planner Agent](planner_agent.md)

Creates research plans tailored to specific companies and industries. The Planner Agent determines what data needs to be collected and analyzed for each company, considering its industry, size, and other factors.

### [Data Collection Agent](data_collection_agent.md)

Gathers financial data from APIs and other sources based on the research plan. This agent interacts with the Financial Data Provider to retrieve comprehensive financial information about the company.

### [Research Agent](research_agent.md)

Conducts web research on industry trends and market news. The Research Agent uses search APIs to gather current information about the company, its competitors, and industry trends that might impact its financial performance.

### [Analysis Agent](analysis_agent.md)

Analyzes financial data to extract insights and identify trends. This agent combines algorithmic financial analysis with LLM-powered qualitative analysis to provide comprehensive insights.

### [Writer Agent](writer_agent.md)

Generates well-structured, professional financial reports. The Writer Agent takes analysis results and transforms them into a coherent, readable report in Markdown format.

### [Fact Check Agent](fact_check_agent.md)

Validates the accuracy of the financial report content. This agent verifies factual claims, adds proper citations, and improves the overall quality of the report.

## Agent Communication

Agents communicate through structured JSON objects that are passed through the Orchestrator. Each agent's output becomes input to the next agent in the workflow:

```
Planner → Data Collection → Research → Analysis → Writer → Fact Check
```

## Extending the Agent System

To add a new agent type to the system:

1. Create a new class that inherits from `BaseAgent`
2. Implement the `process` method to handle specific functionality
3. Add the agent to the Orchestrator workflow

See the [Contributing](../contributing.md) guide for more information on extending the agent system.

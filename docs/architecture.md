# System Architecture

The Financial Analysis System follows a modular architecture based on specialized agents that collaborate to produce financial analysis reports.

## High-Level Architecture

```mermaid
graph TB
    %% Define styles
    classDef agent fill:#E1F5FE,stroke:#0277BD,stroke-width:2px;
    classDef tool fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px;
    classDef data fill:#F5F5F5,stroke:#616161,stroke-width:2px;

    %% User Input
    UserInput["User Input<br/>(Ticker Symbol)"]

    %% Orchestrator
    Orchestrator["Financial Analysis Orchestrator"]
    
    %% Agents
    PlannerAgent["Planner Agent"]:::agent
    DataCollectionAgent["Data Collection<br/>Agent"]:::agent
    ResearchAgent["Research Agent"]:::agent
    AnalysisAgent["Analysis Agent"]:::agent
    WriterAgent["Writer Agent"]:::agent
    FactCheckAgent["Fact Check Agent"]:::agent
    
    %% Tools
    FinancialProvider["Financial<br/>Data Provider"]:::tool
    WebResearch["Web Research"]:::tool
    
    %% Data
    ResearchPlan["Research Plan"]:::data
    FinancialData["Financial Data"]:::data
    ResearchResults["Research Results"]:::data
    AnalysisResults["Analysis Results"]:::data
    Report["Report"]:::data
    FinalReport["Final Report"]:::data

    %% Flow
    UserInput --> Orchestrator
    Orchestrator --> PlannerAgent
    Orchestrator --> DataCollectionAgent
    Orchestrator --> ResearchAgent
    Orchestrator --> AnalysisAgent
    Orchestrator --> WriterAgent
    
    PlannerAgent --> ResearchPlan
    
    DataCollectionAgent --> FinancialProvider
    FinancialProvider --> FinancialData
    
    ResearchAgent --> WebResearch
    WebResearch --> ResearchResults
    
    ResearchPlan --> AnalysisAgent
    FinancialData --> AnalysisAgent
    ResearchResults --> AnalysisAgent
    AnalysisAgent --> AnalysisResults
    AnalysisResults --> WriterAgent
    WriterAgent --> Report
    Report --> FactCheckAgent
    FactCheckAgent --> FinalReport

    %% Add subgraph for visual grouping
    subgraph Agents
        PlannerAgent
        DataCollectionAgent
        ResearchAgent
        AnalysisAgent
        WriterAgent
    end
```

## Workflow

The system follows this workflow:

1. **Orchestrator** receives a ticker symbol and initializes the process
2. **Planner Agent** creates a research plan tailored to the company
3. **Data Collection Agent** gathers financial data based on the plan
4. **Research Agent** conducts web research on the company and industry
5. **Analysis Agent** processes financial data and integrates research insights
6. **Writer Agent** generates a comprehensive financial report
7. **Fact Check Agent** verifies the accuracy of the report
8. **Orchestrator** delivers the final report

## Agent Communication

Agents communicate by passing structured data objects. Each agent takes specific inputs and produces outputs that other agents can consume:

- **Planner Agent**: Takes ticker and company info, outputs research plan
- **Data Collection Agent**: Takes ticker and research plan, outputs financial data
- **Research Agent**: Takes ticker and company profile, outputs research results
- **Analysis Agent**: Takes financial data and research results, outputs analysis
- **Writer Agent**: Takes analysis results, outputs draft report
- **Fact Check Agent**: Takes draft report and data, outputs verified report

## Dependencies

The system relies on several external services and libraries:

- **Financial Data**: Financial Modeling Prep API
- **Web Research**: SerpAPI
- **Natural Language Processing**: OpenAI's LLM API
- **Data Processing**: Pandas and NumPy

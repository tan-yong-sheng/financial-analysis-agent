# Planner Agent

The Planner Agent is responsible for creating detailed research and analysis plans tailored to specific companies. It acts as the initial strategist in the workflow, determining what data needs to be collected and what analyses should be performed.

## Functionality

The Planner Agent:

1. Receives a company ticker symbol and basic company information
2. Creates a comprehensive research plan tailored to the company and its industry
3. Returns a structured plan that guides the rest of the analysis process

## Implementation

The Planner Agent is implemented in the `PlannerAgent` class:

```python
class PlannerAgent(BaseAgent):
    """Agent responsible for creating research and analysis plans."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial planning specialist that creates detailed research and analysis plans"
        super().__init__(role, "Planning Specialist", base_url=base_url, model_name=model_name)
    
    def create_research_plan(self, ticker: str, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a research plan for a given company."""
        # Implementation details...
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to create a research plan."""
        # Implementation details...
```

## Input

The Planner Agent takes a JSON object containing:

```json
{
  "ticker": "AAPL",
  "company_info": {
    "companyName": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."
  }
}
```

## Output

The Planner Agent produces a research plan in JSON format:

```json
{
  "financial_analysis": {
    "income_statement": {
      "focus_areas": ["Revenue growth", "Operating margins", "R&D expenses"],
      "periods": "5-year historical",
      "importance": "high"
    },
    "balance_sheet": {
      "focus_areas": ["Cash reserves", "Debt levels", "Asset growth"],
      "periods": "5-year historical",
      "importance": "medium"
    },
    "cash_flow": {
      "focus_areas": ["Free cash flow", "Capital expenditure", "Share repurchases"],
      "periods": "5-year historical",
      "importance": "high"
    }
  },
  "technical_analysis": {
    "indicators": ["SMA", "EMA", "RSI"],
    "time_periods": ["50-day", "200-day"],
    "importance": "medium"
  },
  "industry_research": {
    "key_competitors": ["Samsung", "Xiaomi", "Google"],
    "market_trends": ["Smartphone market saturation", "Services growth"],
    "importance": "high"
  },
  "report_structure": {
    "sections": [
      "executive_summary",
      "company_overview",
      "industry_analysis",
      "financial_analysis",
      "technical_analysis",
      "risk_assessment",
      "investment_recommendation",
      "appendix"
    ]
  }
}
```

## Key Methods

### `create_research_plan(ticker, company_info)`

Creates a tailored research plan for a specific company by:

1. Analyzing the company's sector and industry
2. Determining which financial metrics are most relevant
3. Identifying what technical indicators to use
4. Planning what industry research is needed
5. Outlining the structure of the final report

### `process(input_data)`

The main entry point that:

1. Validates the input data
2. Extracts the ticker symbol and company information
3. Calls `create_research_plan` to generate the plan
4. Returns the structured plan

## Customization

To customize the Planner Agent for specific industries:

1. Modify the prompt template in `create_research_plan` to include industry-specific guidance
2. Add logic to prioritize different metrics based on industry classification
3. Include additional specialized sections for certain sectors (e.g., regulatory analysis for financial or healthcare companies)

## Example Usage

```python
from agents.planner_agent import PlannerAgent

# Initialize the agent
planner = PlannerAgent()

# Create input data
input_data = {
    "ticker": "AAPL",
    "company_info": {
        "companyName": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }
}

# Generate a research plan
research_plan = planner.process(input_data)

# Use the research plan for subsequent analysis
print(research_plan)
```

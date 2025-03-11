# Research Agent

The Research Agent is responsible for conducting market research, gathering information about companies and industries, and synthesizing this information into actionable insights with robust citation tracking.

## Functionality

The Research Agent:

1. Creates a comprehensive research plan for a company
2. Searches for relevant information across various sources
3. Extracts and synthesizes key findings from articles and reports
4. Analyzes research findings to identify key insights and trends
5. Ensures all insights are properly cited to their sources
6. Returns research results with full citation information

## Implementation

The Research Agent is implemented in the `ResearchAgent` class:

```python
class ResearchAgent(BaseAgent):
    """Agent responsible for conducting web research and finding relevant information."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial research specialist that gathers relevant market news and industry information"
        super().__init__(role, "Research Specialist", base_url=base_url, model_name=model_name)
        self.tracer = AgentTracer("Market Researcher", structured_logger)
    
    def create_research_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive research plan for a company."""
        # Implementation details...
    
    def search_web(self, query: str, num_results: int = MAX_SEARCH_RESULTS) -> List[Dict[str, Any]]:
        """Perform a web search with source tracking."""
        # Implementation details...
    
    def extract_article_content(self, url: str) -> Dict[str, Any]:
        """Extract and summarize content from a URL with source information."""
        # Implementation details...
        
    # Additional methods...
```

## Citation Management

The Research Agent maintains detailed citation information for all research findings:

```python
# Add source information
result["_source"] = {
    "type": "article",
    "url": url,
    "extraction_date": self._get_current_date(),
    "publication_name": self._extract_publication_name(url),
    "publication_date": result.get("publication_date", "Unknown"),
    "citation_format": f"{result.get('title')}. {self._extract_publication_name(url)}. {result.get('publication_date', 'n.d.')}. Retrieved from {url}"
}
```

Each insight is modeled as a `CitableItem` containing both content and citation:

```python
class CitableItem(BaseModel):
    """Model for an item that can have a citation"""
    content: str = Field(description="The content text")
    citation: Optional[str] = Field(description="Citation source", default=None)
```

## Input

The Research Agent takes a JSON object containing:

```json
{
  "ticker": "AAPL",
  "company_data": {
    "companyName": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."
  },
  "research_plan": {
    "key_areas": ["financial_performance", "market_position", "industry_trends"],
    "metrics": ["revenue_growth", "profit_margins", "market_share"],
    "competitors": ["MSFT", "GOOG", "AMZN"],
    "questions": ["How is Apple positioned in the AI market?", "What are the key risks?"]
  }
}
```

## Output

The Research Agent produces structured research findings with citations:

```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "analysis": {
    "market_trends": [
      {
        "content": "The smartphone market is experiencing slowing growth globally, with a 2% decline in shipments in Q2 2023.",
        "citation": "IDC Market Report, 2023-06-15"
      },
      {
        "content": "AI-enabled devices are seeing increased consumer demand, with a 15% premium over standard devices.",
        "citation": "TechAnalyst.com, 2023-07-22"
      }
    ],
    "competitive_position": [
      {
        "content": "Apple maintains premium positioning with 42% market share in the high-end smartphone segment.",
        "citation": "MarketWatch Industry Analysis, 2023-08-10"
      }
    ],
    "risks_opportunities": {
      "risks": [
        {
          "content": "Supply chain constraints in semiconductor components may impact production capacity.",
          "citation": "Bloomberg Supply Chain Report, 2023-07-05"
        }
      ],
      "opportunities": [
        {
          "content": "Expansion into healthcare wearables presents a significant growth opportunity.",
          "citation": "HealthTech Insights, 2023-08-01"
        }
      ]
    },
    "recent_events": [
      {
        "content": "Apple announced new AI features for iOS at their developer conference.",
        "citation": "TechCrunch, 2023-06-06"
      }
    ],
    "industry_outlook": {
      "content": "The premium tech hardware segment is projected to grow 8% annually through 2025.",
      "citation": "Gartner Industry Forecast, 2023-05-30"
    }
  },
  "sources": {
    "search_queries": [
      "Apple Inc. AAPL company overview financial",
      "Apple Inc. AAPL recent financial performance quarterly results",
      "Technology industry trends market analysis Apple Inc."
    ],
    "articles": [
      {
        "type": "article",
        "url": "https://techcrunch.com/2023/06/06/apple-wwdc-ai-features/",
        "extraction_date": "2023-09-01",
        "publication_name": "TechCrunch",
        "publication_date": "2023-06-06"
      },
      // Additional source entries...
    ]
  }
}
```

## Key Methods

### `create_research_plan(input_data)`

Creates a structured research plan using the LLM with the input company information:

```python
plan = self._call_structured_llm(prompt, ResearchPlan)
```

### `conduct_research(research_plan, depth)`

Conducts comprehensive research based on the research plan, tracking all sources:

```python
findings = {
    # Research results...
    "_sources": {  # Track all sources used in the research
        "search_queries": [],
        "articles": []
    }
}
```

### `analyze_research_findings(research_findings, research_plan)`

Analyzes research findings to extract key insights with proper citation:

```python
# Ensure all insights have default citations if missing
for field in ["market_trends", "competitive_position", "recent_events"]:
    if field in analysis_dict:
        for i, item in enumerate(analysis_dict[field]):
            if not item.get("citation"):
                analysis_dict[field][i]["citation"] = "Internal Analysis"
```

## Observability

The Research Agent includes comprehensive observability:

```python
@monitor_agent_method()
def create_research_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    self.tracer.start_task("create_research_plan", ticker=input_data.get("ticker"))
    # Implementation...
    self.tracer.end_task(status="success", result_summary={"ticker": result.get("ticker")})
```

This provides:
- Detailed method execution logging
- Task tracing for complex operations
- Performance metrics for research operations
- Structured error reporting

## Example Usage

```python
from agents.research_agent import ResearchAgent

# Initialize the agent
researcher = ResearchAgent()

# Create input data
input_data = {
    "ticker": "AAPL",
    "company_data": {
        "companyName": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }
}

# Conduct research
research_results = researcher.process(input_data)

# Access insights with citations
market_trends = research_results["analysis"]["market_trends"]
for trend in market_trends:
    print(f"Trend: {trend['content']}")
    print(f"Source: {trend['citation']}")
```

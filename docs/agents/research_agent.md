# Research Agent

The Research Agent is responsible for conducting web research to gather information about companies, industries, and market trends. It uses search APIs to find and analyze relevant news, articles, and data.

## Functionality

The Research Agent:

1. Receives a company ticker, profile information, and research plan
2. Performs targeted web searches for company news, industry trends, and competitor information
3. Analyzes and summarizes the research findings
4. Returns structured research results

## Implementation

The Research Agent is implemented in the `ResearchAgent` class:

```python
class ResearchAgent(BaseAgent):
    """Agent responsible for conducting web research and finding relevant information."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial research specialist that gathers relevant market news and industry information"
        super().__init__(role, "Research Specialist", base_url=base_url, model_name=model_name)
        self.research_tool = WebResearchTool()
    
    def web_search(self, query: str, num_results: int = MAX_SEARCH_RESULTS) -> List[Dict[str, Any]]:
        """Perform a web search using the web research tool."""
        # Implementation details...
    
    def research_company_news(self, ticker: str, company_name: str) -> List[Dict[str, Any]]:
        """Research recent news about a company."""
        # Implementation details...
    
    def research_industry_trends(self, industry: str, sector: str) -> Dict[str, Any]:
        """Research industry trends."""
        # Implementation details...
    
    def research_competitors(self, ticker: str, company_name: str, industry: str) -> Dict[str, Any]:
        """Research company competitors."""
        # Implementation details...
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the research request for a company."""
        # Implementation details...
```

## Input

The Research Agent takes a JSON object containing:

```json
{
  "ticker": "AAPL",
  "company_profile": [{
    "companyName": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics"
  }],
  "research_plan": {
    "industry_research": {
      "key_competitors": ["Samsung", "Xiaomi", "Google"],
      "market_trends": ["Smartphone market saturation", "Services growth"]
    }
  }
}
```

## Output

The Research Agent produces structured research results:

```json
{
  "company_news": [
    {
      "title": "Apple Unveils New AI Features for iPhone",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/apple-ai-features",
      "date": "2023-12-10",
      "summary": "Apple announced new AI capabilities coming to iPhones next year, including improved Siri and on-device processing.",
      "impact": "Medium"
    }
  ],
  "industry_trends": {
    "key_trends": [
      {
        "trend": "AI Integration in Consumer Electronics",
        "description": "Companies are increasingly integrating AI capabilities into consumer electronics.",
        "impact": "Major shift in product development strategies."
      }
    ],
    "growth_prospects": {
      "short_term": "Moderate growth expected due to economic uncertainties.",
      "long_term": "Strong growth projected driven by AI, AR, and new form factors."
    },
    "challenges": [
      "Supply chain constraints",
      "Increasing component costs",
      "Regulatory scrutiny"
    ]
  },
  "competitor_analysis": {
    "competitors": [
      {
        "name": "Samsung Electronics",
        "ticker": "005930.KS",
        "market_share": "19%",
        "strengths": ["Vertical integration", "Display technology leadership"],
        "weaknesses": ["Software ecosystem fragmentation", "Lower brand premium"]
      }
    ],
    "competitive_analysis": {
      "apple_advantages": ["Ecosystem lock-in", "Brand premium", "Service revenue growth"],
      "apple_disadvantages": ["Higher price points", "Limited market share in emerging markets"]
    }
  }
}
```

## Key Methods

### `web_search(query, num_results)`

Performs a general web search using the WebResearchTool:

1. Sends a search query to the search API
2. Processes and formats the search results
3. Returns a list of relevant search results

### `research_company_news(ticker, company_name)`

Researches recent news about a company:

1. Constructs a search query combining company name and ticker
2. Uses news-specific search if available
3. Uses LLM to analyze, summarize, and rate the news items
4. Returns a list of relevant and impactful news items

### `research_industry_trends(industry, sector)`

Researches trends in an industry or sector:

1. Constructs a search query focused on industry trends
2. Uses LLM to analyze search results and extract key trends
3. Structures the information into a comprehensive industry analysis
4. Returns insights about growth prospects, challenges, and competitive landscape

### `research_competitors(ticker, company_name, industry)`

Researches a company's competitors:

1. Constructs a search query focused on competitors
2. Uses LLM to identify and analyze main competitors
3. Compares relative market positions and competitive advantages
4. Returns structured competitor analysis

### `process(input_data)`

The main entry point that:

1. Validates the input data
2. Extracts company information from the input
3. Conducts research on company news, industry trends, and competitors
4. Combines all research results into a structured output

## Search API Integration

The Research Agent uses the WebResearchTool, which integrates with search APIs like SerpAPI to perform web searches. Alternative search providers can be implemented by modifying the WebResearchTool.

## Example Usage

```python
from agents.research_agent import ResearchAgent

# Initialize the agent
researcher = ResearchAgent()

# Create input data
input_data = {
    "ticker": "AAPL",
    "company_profile": [{
        "companyName": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }],
    "research_plan": {
        "industry_research": {
            "key_competitors": ["Samsung", "Xiaomi"]
        }
    }
}

# Conduct research
research_results = researcher.process(input_data)

# Access specific research findings
news = research_results.get("company_news", [])
trends = research_results.get("industry_trends", {})
competitors = research_results.get("competitor_analysis", {})

print(f"Found {len(news)} relevant news items")
print(f"Key industry trend: {trends.get('key_trends', [{}])[0].get('trend', '')}")
```

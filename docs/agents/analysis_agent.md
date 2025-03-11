# Analysis Agent

The Analysis Agent is responsible for analyzing financial data and generating insights. It combines algorithmic financial analysis with LLM-powered qualitative assessments to produce comprehensive financial analysis with proper source citation.

## Functionality

The Analysis Agent:

1. Receives financial data and research results with source information
2. Performs quantitative analysis of financial statements and metrics
3. Uses LLM to generate qualitative insights and interpretations
4. Preserves citation information throughout the analysis process
5. Integrates financial analysis with market research
6. Returns comprehensive analysis results with proper citations

## Implementation

The Analysis Agent is implemented in the `AnalysisAgent` class:

```python
class AnalysisAgent(BaseAgent):
    """Agent responsible for analyzing financial data and generating insights."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial analyst that interprets financial data and identifies key trends and insights"
        super().__init__(role, "Financial Analyst", base_url=base_url, model_name=model_name)
        self.analyzer = FinancialAnalyzer()
    
    def analyze_financial_data(self, financial_data: Dict[str, Any], research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial data based on the research plan."""
        # Implementation details...
    
    def integrate_market_research(self, analysis_results: Dict[str, Any], research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate market research with financial analysis, preserving citations."""
        # Implementation details...
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to analyze financial information."""
        # Implementation details...
```

## Citation Management

The Analysis Agent preserves citation information from both financial data and research results:

```python
def integrate_market_research(self, analysis_results: Dict[str, Any], research_results: Dict[str, Any]) -> Dict[str, Any]:
    # Extract cited insights from research results
    market_trends = research_results.get("analysis", {}).get("market_trends", [])
    competitor_insights = research_results.get("analysis", {}).get("competitive_position", [])
    
    # Integrate with financial analysis while preserving citations
    integrated_insights = {
        "market_financial_connections": []
    }
    
    # Create connections between financial data and market trends, preserving source info
    for trend in market_trends:
        if isinstance(trend, dict) and "content" in trend and "citation" in trend:
            # Connect financial data to market trend with citation
            connection = {
                "content": f"Connection between financial data and market trend: {trend['content']}",
                "citation": trend.get("citation", "Internal Analysis"),
                "related_financial_metric": "revenue growth"  # Example connection
            }
            integrated_insights["market_financial_connections"].append(connection)
            
    return integrated_insights
```

## Input

The Analysis Agent takes a JSON object containing:

```json
{
  "financial_data": {
    "company_profile": {
      "companyName": "Apple Inc.",
      "_source": {
        "name": "Financial Modeling Prep API",
        "endpoint": "profile/AAPL",
        "date_retrieved": "2023-05-15"
      }
    },
    "income_statement": [
      {
        "revenue": 383946000000,
        "_source": {
          "name": "Financial Modeling Prep API",
          "endpoint": "income-statement/AAPL",
          "date_retrieved": "2023-05-15"
        }
      }
    ]
  },
  "research_results": {
    "analysis": {
      "market_trends": [
        {
          "content": "The smartphone market is experiencing slowing growth globally.",
          "citation": "IDC Market Report, 2023-06-15"
        }
      ]
    }
  },
  "sources": {
    "financial_data_sources": {...},
    "research_sources": {...}
  }
}
```

## Output

The Analysis Agent produces comprehensive analysis results with citation information preserved:

```json
{
  "financial_analysis": {
    "quantitative_analysis": {
      "income_analysis": {
        "summary": {
          "latest_revenue": 383946000000,
          "latest_net_income": 96995000000,
          "_source": {
            "name": "Financial Modeling Prep API",
            "endpoint": "income-statement/AAPL",
            "date_retrieved": "2023-05-15"
          }
        },
        "growth": {
          "revenue_growth": 2.02,
          "net_income_growth": -3.36
        },
        "margins": {
          "gross_margin": 46.21,
          "operating_margin": 31.51,
          "profit_margin": 24.79
        }
      }
    },
    "qualitative_analysis": {
      "significant_trends": [
        {
          "content": "Steady revenue growth despite market headwinds",
          "citation": "Internal Analysis based on Financial Modeling Prep API data"
        },
        {
          "content": "Expanding profit margins due to services growth",
          "citation": "Internal Analysis based on Financial Modeling Prep API data"
        }
      ]
    }
  },
  "integrated_insights": {
    "market_financial_connections": [
      {
        "content": "Strong correlation between service revenue growth and industry trend toward subscription models",
        "citation": "MarketWatch Industry Analysis, 2023-08-10",
        "related_financial_metric": "services revenue"
      }
    ],
    "competitive_position": {
      "financial_advantages": [
        {
          "content": "Higher profit margins than industry average (24.79% vs 15.3%)",
          "citation": "Internal Analysis based on Financial Modeling Prep API & IDC Industry Average data"
        }
      ]
    }
  },
  "sources": {
    "financial_data_sources": {...},
    "research_sources": {...}
  },
  "citation_stats": {
    "total_citable_items": 15,
    "items_with_citations": 15, 
    "citation_percentage": 100.0,
    "citation_sources": ["Financial Modeling Prep API", "IDC Market Report", "MarketWatch Industry Analysis", "Internal Analysis"]
  }
}
```

## Key Methods

### `analyze_financial_data(financial_data, research_plan)`

Performs comprehensive analysis of financial data:

1. Uses the FinancialAnalyzer module to perform quantitative analysis
2. Extracts company information from the data
3. Uses LLM to generate qualitative insights about the financial data
4. Combines quantitative metrics with qualitative assessments

### `integrate_market_research(analysis_results, research_results)`

Integrates financial analysis with market research:

1. Identifies connections between financial performance and market events/trends
2. Evaluates how competitive position affects financial results
3. Assesses how industry trends might impact future financial performance
4. Determines if financial data aligns with or contradicts market perception
5. Provides a holistic assessment of the company's position and outlook

### `process(input_data)`

The main entry point that:

1. Validates the input data
2. Extracts financial data, research results, and research plan
3. Analyzes the financial data
4. Integrates with market research if available
5. Returns comprehensive analysis results

## Financial Analysis

The Analysis Agent uses the FinancialAnalyzer module to perform quantitative analysis, which includes:

- Income statement analysis (revenue trends, profit margins, growth rates)
- Balance sheet analysis (liquidity, leverage, asset efficiency)
- Cash flow analysis (operating cash flow, free cash flow, cash usage)
- Technical indicators analysis (moving averages, RSI, etc.)

## JSON Serialization

The Analysis Agent employs special handling for NumPy data types through:

1. The DataTransformer's NumpyEncoder for proper JSON serialization
2. The convert_numpy_types function to ensure all data is JSON-serializable

This prevents common errors like "Object of type int64 is not JSON serializable."

## Example Usage

```python
from agents.analysis_agent import AnalysisAgent

# Initialize the agent
analyst = AnalysisAgent()

# Create input data
input_data = {
    "financial_data": collected_financial_data,
    "research_results": research_results,
    "research_plan": research_plan
}

# Perform analysis
analysis_results = analyst.process(input_data)

# Access analysis components
quantitative = analysis_results.get("financial_analysis", {}).get("quantitative_analysis", {})
qualitative = analysis_results.get("financial_analysis", {}).get("qualitative_analysis", {})
integrated = analysis_results.get("integrated_insights", {})

# Use the analysis results
print(f"Revenue growth: {quantitative.get('income_analysis', {}).get('growth', {}).get('revenue_growth')}%")
print(f"Key strength: {qualitative.get('financial_strengths', [''])[0]}")
```

## Key Methods for Citation Handling

### `analyze_financial_metrics(financial_data)`

Analyzes financial metrics while preserving source information:

```python
def analyze_financial_metrics(self, financial_data):
    # Extract income statement data
    income_statement = financial_data.get("income_statement", [])
    
    if not income_statement or "error" in income_statement[0]:
        return {"error": "No valid income statement data available"}
    
    # Calculate metrics
    analysis = self.analyzer.analyze_income_statement(income_statement)
    
    # Preserve source information
    if income_statement and isinstance(income_statement[0], dict) and "_source" in income_statement[0]:
        source_info = income_statement[0]["_source"]
        analysis["_source"] = source_info
    
    return analysis
```

### `integrate_cited_insights(analysis_results, research_results)`

Integrates research insights with financial analysis while maintaining citations:

```python
def integrate_cited_insights(self, analysis_results, research_results):
    # Get industry_outlook with citation from research
    industry_outlook = research_results.get("analysis", {}).get("industry_outlook", {})
    
    # Get key financial metrics
    revenue_growth = analysis_results.get("quantitative_analysis", {}).get(
        "income_analysis", {}).get("growth", {}).get("revenue_growth")
    
    # Create integrated insight with proper citation
    if industry_outlook and "content" in industry_outlook:
        insight = {
            "content": f"Industry outlook ({industry_outlook['content']}) suggests potential future revenue growth compared to current {revenue_growth}%",
            "citation": industry_outlook.get("citation", "Internal Analysis"),
            "financial_metrics_source": analysis_results.get("quantitative_analysis", {}).get(
                "income_analysis", {}).get("_source", {"name": "Internal Analysis"})
        }
        return insight
```

### `ensure_citation_coverage(analysis_results)`

Ensures all insights have proper citation information:

```python
def ensure_citation_coverage(self, analysis_results):
    # Check qualitative insights for citations
    qualitative = analysis_results.get("qualitative_analysis", {})
    
    for category in qualitative:
        if isinstance(qualitative[category], list):
            for i, item in enumerate(qualitative[category]):
                if isinstance(item, dict) and "content" in item and "citation" not in item:
                    qualitative[category][i]["citation"] = "Internal Analysis"
    
    # Check integrated insights for citations
    integrated = analysis_results.get("integrated_insights", {})
    # Similar process for integrated insights
    
    return analysis_results
```

## Example Usage with Citation Tracking

```python
from agents.analysis_agent import AnalysisAgent
from utils.citation_validator import check_citations_in_analysis

# Initialize the agent
analyst = AnalysisAgent()

# Create input data with sources
input_data = {
    "financial_data": financial_data_with_sources,
    "research_results": research_results_with_citations,
    "research_plan": research_plan,
    "sources": {
        "financial_data_sources": financial_sources,
        "research_sources": research_sources
    }
}

# Perform analysis
analysis_results = analyst.process(input_data)

# Check citation coverage
citation_stats = check_citations_in_analysis(analysis_results)
print(f"Citation coverage: {citation_stats['citation_percentage']}%")
print(f"Sources used: {citation_stats['citation_sources']}")

# Access analysis with citations
for trend in analysis_results["qualitative_analysis"]["significant_trends"]:
    print(f"Trend: {trend['content']}")
    print(f"Source: {trend['citation']}")
```

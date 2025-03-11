# Citation System

The Financial Analysis Agent includes a comprehensive citation system that ensures all data and insights are properly attributed to their sources, enhancing the credibility and traceability of financial analysis.

## Overview

The citation system tracks the origin of all financial data and research insights throughout the analysis pipeline:

1. **Data Collection**: All financial data includes source information
2. **Market Research**: All insights include proper citations
3. **Analysis**: Insights preserve citation information
4. **Report Generation**: Citations appear in the final report

## Implementation

### Source Tracking for Financial Data

Financial data includes `_source` fields with detailed provenance information:

```python
data["_source"] = {
    "name": "Financial Modeling Prep API",
    "endpoint": f"income-statement/{ticker}",
    "period": period,
    "date_retrieved": self._get_current_date(),
    "url": url.split('?')[0]
}
```

### Citation Models

The system uses Pydantic models to enforce proper citation structure:

```python
class CitableItem(BaseModel):
    """Model for an item that can have a citation"""
    content: str = Field(description="The content text")
    citation: Optional[str] = Field(description="Citation source", default=None)

class SourceInfo(BaseModel):
    """Model for tracking source information"""
    name: str = Field(description="Name of the source")
    type: str = Field(description="Type of source (API, article, search)")
    date_retrieved: str = Field(description="Date the information was retrieved")
    url: Optional[str] = Field(description="URL of the source if applicable", default=None)
    details: Optional[Dict[str, Any]] = Field(description="Additional source details", default_factory=dict)
    filing_info: Optional[Dict[str, str]] = Field(description="SEC filing information if applicable", default=None)
```

### Citation Validation

The system includes utilities for citation validation:

```python
def check_citations_in_analysis(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """Check if citations are present in analysis results."""
    stats = {
        "total_citable_items": 0,
        "items_with_citations": 0,
        "citation_sources": set()
    }
    
    # Check each citable item
    def _check_item(item):
        if isinstance(item, dict) and "content" in item:
            stats["total_citable_items"] += 1
            if "citation" in item and item["citation"]:
                stats["items_with_citations"] += 1
                if item["citation"] != "Internal Analysis":
                    stats["citation_sources"].add(item["citation"])
    
    # Check all sections
    # ...
```

## Citation Guidelines

### Financial Data Citation

Financial data should include:

1. **Source name**: The API or data provider
2. **Retrieval date**: When the data was collected
3. **Endpoint**: Specific API endpoint used
4. **Period**: Time period of the financial data
5. **URL**: Source URL without authentication details

### Research Citation

Research insights should include:

1. **Publication name**: Source publication
2. **Publication date**: When the source was published
3. **URL**: Original source URL
4. **Authors**: Original authors when available

### Citation Format

Standard citation format in reports:

```
Financial data: [Financial Modeling Prep API, retrieved 2023-05-15]
News articles: [Bloomberg, 2023-06-10]
SEC filings: [10-K Annual Report, filed 2023-01-25]
```

## Source Types

The system tracks various source types:

1. **Financial APIs**: Financial statements, metrics, and prices
2. **News Publications**: Articles and press releases
3. **Official Filings**: SEC documents and regulatory filings
4. **Analyst Reports**: Professional financial analysis
5. **Internal Analysis**: System-generated insights

## Citation Flow

The citation system maintains source information through the entire workflow:

1. **Data Collection Agent**: Attaches `_source` to all collected data
2. **Research Agent**: Creates `CitableItem` instances with citations
3. **Analysis Agent**: Preserves citations when combining information
4. **Orchestrator**: Consolidates source information
5. **Report Agent**: Formats citations in the final report
6. **Fact Check Agent**: Validates citation quality

## Example Usage

Accessing citation information in the analysis results:

```python
# Get market trends with citations
trends = analysis_results["analysis"]["market_trends"]
for trend in trends:
    print(f"Trend: {trend['content']}")
    print(f"Source: {trend['citation']}")

# Check citation statistics
citation_stats = analysis_results["citation_stats"]
print(f"Citation coverage: {citation_stats['citation_percentage']}%")
print(f"Sources used: {citation_stats['citation_sources']}")
```

## Benefits

The citation system provides:

1. **Credibility**: Properly attributed insights increase trustworthiness
2. **Traceability**: All data can be traced back to original sources
3. **Verifiability**: Claims can be verified against original sources
4. **Compliance**: Meets regulatory requirements for financial analysis
5. **Transparency**: Users understand where information originated

## Future Extensions

Planned enhancements to the citation system:

1. **SEC filing-specific attribution**: Detailed tracking of filing types, periods, etc.
2. **Citation confidence scores**: Rating the reliability of different sources
3. **Timeline-aware citation**: Managing superseded information
4. **Citation network visualization**: Visual representation of source relationships

# Citation Guidelines for Financial Analysis

This document outlines the citation system used in the Financial Analysis Agent to ensure transparency, reliability, and traceability of financial information.

## Source Types

The system tracks several types of sources:

1. **API Data Sources**
   - Financial statement data from APIs
   - Technical indicators
   - Company profile information
   
2. **Research Sources**
   - News articles and press releases
   - Analyst reports
   - Industry research
   
3. **Generated Analysis**
   - Generated content marked with "Internal Analysis" citation

## Citation Format

### Financial Data Citations
```json
{
  "_source": {
    "name": "Financial Modeling Prep API",
    "endpoint": "income-statement/AAPL",
    "period": "annual",
    "date_retrieved": "2023-05-15"
  }
}
```

### Research Citations
```json
{
  "content": "Apple showed strong growth in services revenue...",
  "citation": "Bloomberg Technology, 2023-04-12"
}
```

## Implementation Details

1. The `DataCollectionAgent` attaches `_source` fields to all retrieved financial data
2. The `ResearchAgent` uses `CitableItem` objects to pair content with citations
3. The `AnalysisAgent` preserves citations when combining information
4. The `ReportAgent` includes citations in the final report

## Best Practices

- Always cite the original source of financial data
- Include retrieval dates for all financial information
- Distinguish between primary sources (SEC filings) and secondary sources
- Maintain the audit trail throughout the analysis pipeline

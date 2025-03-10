# Fact Check Agent

The Fact Check Agent is responsible for validating the accuracy of the financial analysis report. It acts as a quality control component, verifying factual claims and improving the report's accuracy and credibility.

## Functionality

The Fact Check Agent:

1. Receives the draft report along with the financial data and analysis results
2. Validates financial data and claims in the report against source data
3. Identifies uncited claims or statements that require verification
4. Adds appropriate citations to factual statements
5. Returns an improved version of the report with validation results

## Implementation

The Fact Check Agent is implemented in the `FactCheckAgent` class:

```python
class FactCheckAgent(BaseAgent):
    """Agent responsible for fact-checking and validating reports."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial fact-checking specialist that verifies and validates financial information"
        super().__init__(role, "Fact Checker", base_url=base_url, model_name=model_name)
    
    def validate_financial_data(self, financial_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the financial data and analysis results for accuracy."""
        # Implementation details...
    
    def check_citations(self, report_content: str, financial_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check that all factual claims in the report are properly cited."""
        # Implementation details...
    
    def add_citations(self, report_content: str, financial_data_sources: Dict[str, str]) -> str:
        """Add proper citations to the report content."""
        # Implementation details...
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to fact check and validate the analysis and report."""
        # Implementation details...
```

## Input

The Fact Check Agent takes a JSON object containing:

```json
{
  "report": "# Financial Analysis: Apple Inc. (AAPL)\n\n**Date:** March 10, 2025\n\n## Executive Summary\n\n...",
  "financial_data": {
    "income_statement": [...],
    "balance_sheet": [...],
    "cash_flow": [...],
    "stock_price": {...},
    "technical_indicators": {...}
  },
  "analysis_results": {
    "financial_analysis": {...},
    "market_research": {...},
    "integrated_insights": {...}
  },
  "research_results": {
    "company_news": [...],
    "industry_trends": {...},
    "competitor_analysis": {...}
  }
}
```

## Output

The Fact Check Agent produces validation results and an improved report:

```json
{
  "validation_results": {
    "is_valid": true,
    "issues": [
      "Missing citation for revenue growth claim in Executive Summary"
    ],
    "warnings": [
      "Industry comparison data is from 2024, more recent data may be available"
    ]
  },
  "citation_results": {
    "citation_quality": "fair",
    "uncited_claims_count": 3,
    "incorrect_claims_count": 1,
    "details": {
      "properly_cited_claims": [...],
      "uncited_claims": [...],
      "incorrect_claims": [...],
      "recommendations": [...]
    }
  },
  "improved_report": "# Financial Analysis: Apple Inc. (AAPL)\n\n**Date:** March 10, 2025\n\n## Executive Summary\n\n...[improved report with citations]..."
}
```

## Key Methods

### `validate_financial_data(financial_data, analysis_results)`

Validates the accuracy of the financial data and analysis:

1. Checks for missing required financial data sections
2. Verifies that the analysis structure is valid and complete
3. Conducts basic accounting validation (e.g., revenue should exceed net income)
4. Identifies potential inconsistencies or errors in the data
5. Returns a validation result with any issues or warnings found

### `check_citations(report_content, financial_data, research_data)`

Analyzes the report for proper citation of factual claims:

1. Identifies numerical claims and factual statements in the report
2. Determines whether each claim is properly cited or referenced
3. Verifies that cited claims match the underlying financial data
4. Identifies important financial figures that lack citations
5. Returns a comprehensive citation analysis with recommendations

### `add_citations(report_content, financial_data_sources)`

Improves the report by adding proper citations:

1. Adds superscript citation references to factual claims
2. Maintains the original formatting and structure of the report
3. Adds a "Sources" or "References" section listing all citations
4. Returns the enhanced report with proper citations

### `process(input_data)`

The main entry point that:

1. Validates the input data
2. Extracts the report, financial data, analysis results, and research results
3. Validates the financial data and analysis
4. Checks citations in the report
5. Adds or improves citations if needed
6. Returns validation results and the improved report

## Validation Types

The Fact Check Agent performs several types of validation:

### 1. Data Completeness

Ensures that all required financial data is present:
- Income statement, balance sheet, and cash flow statements
- Stock price data
- Company profile information

### 2. Data Consistency

Checks for logical consistency in financial data:
- Revenue should be greater than or equal to net income
- Assets should equal liabilities plus equity
- Operating cash flow should be consistent with reported income

### 3. Citation Validation

Evaluates the proper attribution of facts and figures:
- Numerical claims should have sources
- Important financial metrics should be cited
- Cited figures should match source data

### 4. Logical Coherence

Ensures that conclusions drawn in the report are supported by the data presented.

## Example Usage

```python
from agents.fact_check_agent import FactCheckAgent

# Initialize the agent
fact_checker = FactCheckAgent()

# Create input data
input_data = {
    "report": draft_report,
    "financial_data": financial_data,
    "analysis_results": analysis_results,
    "research_results": research_results
}

# Fact check the report
fact_check_results = fact_checker.process(input_data)

# Access validation results
validation = fact_check_results["validation_results"]
if validation["is_valid"]:
    print("Report passed validation with", len(validation["warnings"]), "warnings")
else:
    print("Report failed validation with", len(validation["issues"]), "issues")

# Get the improved report
improved_report = fact_check_results["improved_report"]

# Save the improved report
with open("final_report.md", "w") as f:
    f.write(improved_report)
```

The Fact Check Agent is the final quality control step in the report generation process, ensuring that the financial analysis reports produced by the system maintain a high standard of accuracy and proper attribution.

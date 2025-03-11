# Writer Agent

The Writer Agent is responsible for transforming analysis results into a well-structured, professional financial report. This agent takes complex financial data and insights and presents them in a clear, readable format suitable for various audiences.

## Functionality

The Writer Agent:

1. Receives analysis results and company information
2. Generates a detailed report structure based on the research plan
3. Writes individual sections with appropriate content and formatting
4. Combines sections into a cohesive, professional report
5. Returns the complete report in Markdown format

## Implementation

The Writer Agent is implemented in the `WriterAgent` class:

```python
class WriterAgent(BaseAgent):
    """Agent responsible for writing financial research reports."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a professional financial writer that creates clear, insightful financial research reports"
        super().__init__(role, "Financial Writer", base_url=base_url, model_name=model_name)
    
    def generate_report_structure(self, ticker: str, company_info: Dict[str, Any], research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the structure of the financial research report."""
        # Implementation details...
    
    def write_report_section(self, section_name: str, section_template: Dict[str, Any], analysis_data: Dict[str, Any]) -> str:
        """Write a specific section of the report."""
        # Implementation details...
    
    def compile_full_report(self, report_template: Dict[str, Any], section_contents: Dict[str, str]) -> str:
        """Compile all sections into a complete report."""
        # Implementation details...
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to create a financial research report."""
        # Implementation details...
```

## Input

The Writer Agent takes a JSON object containing:

```json
{
  "ticker": "AAPL",
  "company_profile": [{
    "companyName": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."
  }],
  "research_plan": {
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
  },
  "analysis_results": {
    "financial_analysis": {
      "quantitative_analysis": {...},
      "qualitative_analysis": {...}
    },
    "market_research": {...},
    "integrated_insights": {...}
  }
}
```

## Output

The Writer Agent produces a structured output containing:

```json
{
  "report": "# Financial Analysis: Apple Inc. (AAPL)\n\n**Date:** March 10, 2025\n\n## Executive Summary\n\n...[full markdown report content]...",
  "sections": {
    "executive_summary": "Apple Inc. continues to maintain its position as a leader...",
    "financial_analysis": "## Financial Analysis\n\nApple reported total revenue of...",
    "...": "..."
  },
  "structure": {
    "title": "Financial Analysis: Apple Inc. (AAPL)",
    "date": "March 10, 2025",
    "structure": {
      "executive_summary": {
        "title": "Executive Summary",
        "key_points": ["Overview of findings", "Key investment highlights"]
      },
      "...": "..."
    }
  }
}
```

## Key Methods

### `generate_report_structure(ticker, company_info, research_plan)`

Creates a detailed structure for the report:

1. Uses the research plan to determine the appropriate sections
2. Gets LLM guidance for what should be included in each section
3. Structures the report with appropriate titles, key points, and subsections
4. Returns a complete report template that guides the writing process

### `write_report_section(section_name, section_template, analysis_data)`

Writes individual report sections:

1. Identifies the relevant data needed for the section
2. Uses LLM to write professional, analytical content for the section
3. Formats the content appropriately with Markdown
4. Returns the completed section content

### `compile_full_report(report_template, section_contents)`

Combines individual sections into a cohesive report:

1. Creates a title and date header
2. Builds a table of contents with links
3. Combines all section contents in the appropriate order
4. Adds proper formatting and separators between sections
5. Includes a disclaimer at the end
6. Returns the complete Markdown report

### `process(input_data)`

The main entry point that:

1. Validates the input data
2. Extracts the ticker, company profile, research plan, and analysis results
3. Generates the report structure
4. Writes each section of the report
5. Compiles the full report
6. Returns the complete report along with section contents and structure

## Report Formatting

The Writer Agent uses Markdown formatting for the report, which offers several advantages:

1. **Readability**: Clean, structured format that's easy to read in raw form
2. **Convertibility**: Can be easily converted to HTML, PDF, or other formats
3. **Version Control**: Text-based format works well with version control systems
4. **Embeddable**: Code blocks, tables, and charts can be embedded seamlessly

A typical report structure includes:

- **Title and Date**: Report title with company name and ticker
- **Table of Contents**: Links to each major section
- **Executive Summary**: Overview of key findings and recommendations
- **Analytical Sections**: Detailed analysis of different aspects
- **Recommendation**: Clear investment guidance with rationale
- **Appendix/References**: Supporting information and data sources

## Example Usage

```python
from agents.writer_agent import WriterAgent

# Initialize the agent
writer = WriterAgent()

# Create input data
input_data = {
    "ticker": "AAPL",
    "company_profile": [{
        "companyName": "Apple Inc.",
        "sector": "Technology"
    }],
    "research_plan": research_plan,
    "analysis_results": analysis_results
}

# Generate the report
report_results = writer.process(input_data)

# Access the complete report
report_markdown = report_results["report"]

# Save to file
with open("apple_analysis_report.md", "w") as f:
    f.write(report_markdown)
```

The Writer Agent specializes in transforming complex financial analysis into clear, actionable reports that maintain professional standards while being accessible to the intended audience.

import pytest
import json
from unittest.mock import patch, MagicMock
from agents.report_agent import ReportAgent

class TestReportAgent:
    """Tests for the ReportAgent class."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.agent = ReportAgent(base_url="mock_url", model_name="mock_model")
    
    @patch('agents.report_agent.BaseAgent._call_llm')
    def test_generate_report(self, mock_call_llm, sample_financial_data):
        """Test report generation with mocked LLM response."""
        # Setup mock
        mock_markdown = """
# Financial Analysis Report

## Executive Summary
This is a test report summary.

## Financial Analysis
Test financial data analysis.

## Investment Recommendation
Test recommendation.
"""
        mock_call_llm.return_value = mock_markdown
        
        # Call method
        report = self.agent.generate_report(sample_financial_data, "TEST")
        
        # Assertions
        assert "Financial Analysis Report" in report
        assert "Executive Summary" in report
        assert "Financial Analysis" in report
        assert "Investment Recommendation" in report
        
        # Verify LLM was called with proper data
        mock_call_llm.assert_called_once()
        call_args = mock_call_llm.call_args[0][0]
        assert "TEST" in call_args
    
    @patch('agents.report_agent.BaseAgent._call_llm')
    def test_fact_check_report(self, mock_call_llm, sample_financial_data):
        """Test fact checking of reports."""
        # Setup
        mock_report = "# Financial Report\n\nRevenue: $900,000"
        mock_corrected = "# Financial Report\n\nRevenue: $1,000,000"
        mock_call_llm.return_value = mock_corrected
        
        # Call method
        result = self.agent.fact_check_report(mock_report, sample_financial_data)
        
        # Assertions
        assert result == mock_corrected
        assert "$1,000,000" in result  # Should contain the corrected value
    
    def test_clean_markdown(self):
        """Test cleaning of markdown content."""
        # Markdown with various formatting issues
        dirty_markdown = """
```markdown
# Title

## Section
Some content.
## Duplicate Section
```

More content.

# Another Title
"""
        # Clean the markdown
        clean = self.agent._clean_markdown(dirty_markdown)
        
        # Assertions
        assert "```markdown" not in clean
        assert "```" not in clean
        assert "# Title" in clean
        assert "## Section" in clean
        assert "## Duplicate Section" in clean
    
    @patch('agents.report_agent.BaseAgent._call_llm')
    def test_process(self, mock_call_llm, sample_financial_data):
        """Test the complete process method."""
        # Setup mocks
        mock_call_llm.return_value = "# Test Report"
        
        # Call process
        result = self.agent.process({
            "analysis_results": sample_financial_data,
            "ticker": "TEST"
        })
        
        # Assertions
        assert result["ticker"] == "TEST"
        assert "# Test Report" in result["report"]
        assert result["report_file_path"] == "reports/TEST_analysis.md"

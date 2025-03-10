import sys
import os
import json
from typing import Dict, Any, List
import re

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent
from tools.data_transformer import prepare_data_for_report

class ReportAgent(BaseAgent):
    """Agent responsible for generating financial reports in markdown format."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial report writer that creates clear, properly formatted markdown reports"
        super().__init__(role, "Report Writer", base_url=base_url, model_name=model_name)
        
    def generate_report(self, analysis_results: Dict[str, Any], ticker: str) -> str:
        """
        Generate a financial analysis report in markdown format.
        
        Args:
            analysis_results (dict): The analysis results to include in the report.
            ticker (str): The stock ticker symbol.
            
        Returns:
            str: The markdown report.
        """
        # Prepare data for the report
        report_data = prepare_data_for_report(analysis_results)
        
        # Generate report structure with LLM
        prompt = f"""
        Create a comprehensive financial analysis report for {ticker} based on the following analysis data:
        
        {json.dumps(report_data, indent=2)}
        
        The report should include:
        1. An executive summary
        2. Detailed financial analysis covering income statement, balance sheet, and cash flow
        3. Technical analysis if available
        4. An investment recommendation
        5. Risks and opportunities
        
        FORMAT REQUIREMENTS - CRITICALLY IMPORTANT:
        - Format the report as clean markdown with proper heading levels
        - Use # for title, ## for main sections, ### for subsections
        - DO NOT include markdown code block delimiters (```)
        - Make sure all tables are properly formatted with | and - characters
        - Include proper spacing between sections
        """
        
        # Get the raw markdown content
        markdown_content = self._call_llm(prompt)
        
        # Clean up the markdown to fix common formatting issues
        cleaned_markdown = self._clean_markdown(markdown_content)
        
        return cleaned_markdown
        
    def _clean_markdown(self, markdown: str) -> str:
        """
        Clean up markdown content to fix formatting issues.
        
        Args:
            markdown (str): The markdown content to clean.
            
        Returns:
            str: The cleaned markdown content.
        """
        # Remove any markdown code blocks (```markdown ... ```)
        cleaned_md = re.sub(r'```markdown\s*\n', '', markdown)
        cleaned_md = re.sub(r'```\s*\n', '', cleaned_md)
        
        # Fix duplicate headings by finding patterns like "## Section\n## Section"
        cleaned_md = re.sub(r'(#{2,}\s+[^\n]+)\n\1', r'\1', cleaned_md)
        
        # Ensure proper spacing before headers (## should have blank line before)
        cleaned_md = re.sub(r'([^\n])\n(#{2,}\s+)', r'\1\n\n\2', cleaned_md)
        
        # Ensure proper spacing after headers
        cleaned_md = re.sub(r'(#{2,}\s+[^\n]+)\n([^\n#])', r'\1\n\n\2', cleaned_md)
        
        # Remove any trailing backticks that might be left over
        cleaned_md = cleaned_md.replace('```', '')
        
        # Ensure proper spacing between sections
        cleaned_md = re.sub(r'\n{3,}', '\n\n', cleaned_md)
        
        return cleaned_md
    
    def fact_check_report(self, report: str, analysis_results: Dict[str, Any]) -> str:
        """
        Fact check the generated report against the analysis results.
        
        Args:
            report (str): The generated report.
            analysis_results (dict): The analysis results.
            
        Returns:
            str: The fact-checked report with corrections if needed.
        """
        # Prepare data for fact checking
        fact_check_data = prepare_data_for_report(analysis_results)
        
        prompt = f"""
        You are reviewing a financial analysis report for factual accuracy.
        
        Here's the report:
        ---
        {report}
        ---
        
        Here's the analysis data that should be reflected in the report:
        {json.dumps(fact_check_data, indent=2)}
        
        Please verify that all facts, figures, and financial data in the report accurately match the analysis data.
        If you find any discrepancies or factual errors:
        1. Correct the errors
        2. Make sure your corrections maintain proper markdown formatting
        3. Do NOT use markdown code blocks in your response
        
        Return the corrected report as clean markdown text.
        """
        
        corrected_report = self._call_llm(prompt)
        
        # Clean up the corrected report
        return self._clean_markdown(corrected_report)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data to generate a financial analysis report.
        
        Args:
            input_data (dict): Input data containing analysis results and ticker.
            
        Returns:
            dict: Process results including the generated report.
        """
        analysis_results = input_data.get("analysis_results", {})
        ticker = input_data.get("ticker", "UNKNOWN")
        
        if not analysis_results:
            return {"error": "No analysis results provided for report generation"}
        
        # Generate initial report
        report = self.generate_report(analysis_results, ticker)
        
        # Fact check the report
        fact_checked_report = self.fact_check_report(report, analysis_results)
        
        return {
            "ticker": ticker,
            "report": fact_checked_report,
            "report_file_path": f"reports/{ticker}_analysis.md"
        }

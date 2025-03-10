import sys
import os
import json
from typing import Dict, Any, List, Tuple

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent

class FactCheckAgent(BaseAgent):
    """Agent responsible for fact-checking and validating reports."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial fact-checking specialist that verifies and validates financial information"
        super().__init__(role, "Fact Checker", base_url=base_url, model_name=model_name)
    
    def validate_financial_data(self, financial_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the financial data and analysis results for accuracy.
        
        Args:
            financial_data (dict): The collected financial data.
            analysis_results (dict): The analysis results.
            
        Returns:
            dict: Validation results.
        """
        validation_results = {
            "is_valid": True,
            "issues": [],
            "warnings": []
        }
        
        # Check for missing data
        required_sections = ["income_statement", "balance_sheet", "cash_flow", "stock_price"]
        for section in required_sections:
            if section not in financial_data:
                validation_results["issues"].append(f"Missing {section} data")
                validation_results["is_valid"] = False
        
        # Check for inconsistencies in analysis
        try:
            if "income_analysis" in analysis_results.get("quantitative_analysis", {}):
                income_analysis = analysis_results["quantitative_analysis"]["income_analysis"]
                if "error" in income_analysis:
                    validation_results["issues"].append(f"Income statement analysis error: {income_analysis['error']}")
                    validation_results["is_valid"] = False
        except (KeyError, TypeError):
            validation_results["issues"].append("Income statement analysis structure is invalid")
            validation_results["is_valid"] = False
        
        # Check financial data validity (basic checks)
        if "income_statement" in financial_data and financial_data["income_statement"]:
            try:
                for statement in financial_data["income_statement"]:
                    # Check that revenue is greater than or equal to net income (basic accounting check)
                    if "revenue" in statement and "netIncome" in statement:
                        if statement["revenue"] < statement["netIncome"]:
                            validation_results["issues"].append(
                                f"Data inconsistency: Revenue ({statement['revenue']}) less than Net Income ({statement['netIncome']})"
                            )
                            validation_results["is_valid"] = False
            except (TypeError, KeyError):
                validation_results["warnings"].append("Could not validate income statement data structure")
        
        return validation_results
    
    def check_citations(self, report_content: str, financial_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check that all factual claims in the report are properly cited.
        
        Args:
            report_content (str): The content of the report.
            financial_data (dict): The financial data used.
            research_data (dict): The research data used.
            
        Returns:
            dict: Citation check results.
        """
        # Parse report to extract numerical claims and references
        prompt = f"""
        Review this financial report and identify all specific numerical claims and facts:
        
        {report_content[:15000]}  # Limit length to avoid token limits
        
        For each specific numerical claim or fact, determine:
        1. Whether it is properly cited or referenced
        2. Whether the claim matches the underlying financial data
        3. If any important financial figures appear to be missing citations
        
        Format your response as a JSON with:
        - "properly_cited_claims": list of claims that are properly cited
        - "uncited_claims": list of claims that should have citations but don't
        - "incorrect_claims": list of claims that don't match the underlying data
        - "recommendations": specific recommendations for improving citations
        """
        
        try:
            response = self._call_llm(prompt)
            citation_results = json.loads(response)
            
            # Determine overall citation quality
            uncited_count = len(citation_results.get("uncited_claims", []))
            incorrect_count = len(citation_results.get("incorrect_claims", []))
            
            citation_status = {
                "citation_quality": "good" if uncited_count + incorrect_count == 0 else 
                                   "fair" if uncited_count + incorrect_count < 5 else "poor",
                "uncited_claims_count": uncited_count,
                "incorrect_claims_count": incorrect_count,
                "details": citation_results
            }
            
            return citation_status
        except json.JSONDecodeError:
            return {
                "citation_quality": "unknown",
                "error": "Failed to parse citation analysis",
                "details": {}
            }
    
    def add_citations(self, report_content: str, financial_data_sources: Dict[str, str]) -> str:
        """
        Add proper citations to the report content.
        
        Args:
            report_content (str): The content of the report.
            financial_data_sources (dict): The sources of financial data.
            
        Returns:
            str: Report content with added citations.
        """
        sources_info = "\n\n## Data Sources\n\n"
        for source_name, source_details in financial_data_sources.items():
            sources_info += f"- {source_name}: {source_details}\n"
        
        prompt = f"""
        Add proper citations to this financial report. For each numerical claim or statement of fact,
        add a superscript citation reference where appropriate.
        
        Here are the available data sources to cite:
        {json.dumps(financial_data_sources, indent=2)}
        
        Original report:
        {report_content}
        
        Guidelines:
        1. Use superscript numbers for citations (e.g., "Revenue increased by 12%[1]")
        2. Only add citations for specific factual claims or numerical data
        3. Maintain the original formatting and structure of the report
        4. Add a "Sources" section at the end listing all the references
        
        Return the full report with appropriate citations added.
        """
        
        try:
            cited_content = self._call_llm(prompt)
            
            # Ensure we have a Sources section
            if "## Sources" not in cited_content and "## References" not in cited_content:
                cited_content += sources_info
                
            return cited_content
        except Exception as e:
            # If citation addition fails, return original with appended sources
            return report_content + "\n\n" + sources_info
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data to fact check and validate the analysis and report.
        
        Args:
            input_data (dict): Input data containing the report, financial data, and analysis.
            
        Returns:
            dict: Validation results and improved report.
        """
        report = input_data.get("report", "")
        financial_data = input_data.get("financial_data", {})
        analysis_results = input_data.get("analysis_results", {})
        research_data = input_data.get("research_results", {})
        
        # Define data sources
        financial_data_sources = {
            "Financial Statements": "Financial Modeling Prep API, quarterly and annual reports",
            "Stock Price Data": "Financial Modeling Prep API, historical price data",
            "Technical Indicators": "Calculated based on historical price data from Financial Modeling Prep",
            "Industry Analysis": "Web research from industry publications and analyst reports",
            "Company News": "Recent news articles and press releases"
        }
        
        # Validate financial data and analysis
        validation_results = self.validate_financial_data(financial_data, analysis_results)
        
        # Check citations if we have a report
        citation_results = {}
        improved_report = report
        if report:
            citation_results = self.check_citations(report, financial_data, research_data)
            
            # Add citations if needed
            if citation_results.get("citation_quality") != "good":
                improved_report = self.add_citations(report, financial_data_sources)
        
        return {
            "validation_results": validation_results,
            "citation_results": citation_results,
            "improved_report": improved_report
        }

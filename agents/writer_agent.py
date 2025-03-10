import sys
import os
import json
from typing import Dict, Any, List
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent

class WriterAgent(BaseAgent):
    """Agent responsible for writing financial research reports."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a professional financial writer that creates clear, insightful financial research reports"
        super().__init__(role, "Financial Writer", base_url=base_url, model_name=model_name)
    
    def generate_report_structure(self, ticker: str, company_info: Dict[str, Any], research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate the structure of the financial research report.
        
        Args:
            ticker (str): The ticker symbol of the company.
            company_info (dict): Basic company information.
            research_plan (dict): The research plan with report structure recommendations.
            
        Returns:
            dict: Report structure template.
        """
        company_name = company_info.get("companyName", "the company")
        
        # Extract structure from research plan if available
        report_structure = research_plan.get("report_structure", {})
        if not report_structure:
            # Default structure if none specified in plan
            report_structure = {
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
        
        # Generate detailed structure with LLM
        prompt = f"""
        Create a detailed report structure for a financial analysis report on {company_name} ({ticker}).
        
        The basic outline from our research plan includes these sections:
        {json.dumps(report_structure, indent=2)}
        
        For each section, provide:
        1. A title
        2. Key points that should be covered
        3. Specific subsections (if applicable)
        4. Data visualizations that would enhance this section
        
        Format your response as a structured JSON with each major section as a key, 
        and include guidance for what should be included in each section.
        """
        
        try:
            response = self._call_llm(prompt)
            detailed_structure = json.loads(response)
            
            # Create report template
            report_template = {
                "title": f"Financial Analysis: {company_name} ({ticker})",
                "date": datetime.now().strftime("%B %d, %Y"),
                "structure": detailed_structure
            }
            
            return report_template
        except json.JSONDecodeError:
            # Basic template if LLM response isn't valid JSON
            return {
                "title": f"Financial Analysis: {company_name} ({ticker})",
                "date": datetime.now().strftime("%B %d, %Y"),
                "structure": {
                    "executive_summary": {
                        "title": "Executive Summary",
                        "key_points": ["Overview of findings", "Key investment highlights", "Recommendation summary"]
                    },
                    "financial_analysis": {
                        "title": "Financial Analysis",
                        "key_points": ["Income statement analysis", "Balance sheet analysis", "Cash flow analysis"]
                    },
                    "investment_recommendation": {
                        "title": "Investment Recommendation",
                        "key_points": ["Rating", "Price target", "Key factors", "Risks"]
                    }
                }
            }
    
    def write_report_section(self, section_name: str, section_template: Dict[str, Any], 
                             analysis_data: Dict[str, Any]) -> str:
        """
        Write a specific section of the report.
        
        Args:
            section_name (str): The name of the section.
            section_template (dict): Template/structure for this section.
            analysis_data (dict): Relevant analysis data for this section.
            
        Returns:
            str: The written section content in Markdown format.
        """
        title = section_template.get("title", section_name.replace("_", " ").title())
        key_points = section_template.get("key_points", [])
        
        # Extract relevant data for this section
        relevant_data = {}
        if section_name == "financial_analysis" and "financial_analysis" in analysis_data:
            relevant_data = analysis_data["financial_analysis"]
        elif section_name == "technical_analysis" and "quantitative_analysis" in analysis_data:
            relevant_data = analysis_data.get("quantitative_analysis", {}).get("technical_analysis", {})
        elif section_name == "industry_analysis" and "market_research" in analysis_data:
            relevant_data = analysis_data.get("market_research", {}).get("industry_trends", {})
        elif section_name == "risk_assessment" and "integrated_insights" in analysis_data:
            relevant_data = analysis_data.get("integrated_insights", {}).get("risk_assessment", {})
        
        prompt = f"""
        Write a professional financial report section titled "{title}" in Markdown format.
        
        Key points to cover:
        {json.dumps(key_points, indent=2)}
        
        Relevant data:
        {json.dumps(relevant_data, indent=2)}
        
        Guidelines:
        - Write in a professional, analytical tone appropriate for financial analysis
        - Include specific data points from the analysis where relevant
        - Draw meaningful conclusions and insights from the data
        - Be concise but comprehensive, focusing on what matters to investors
        - Use proper financial terminology and industry-specific language
        - Format your response using proper Markdown formatting:
          - Use ## for section headings
          - Use ### for subsections
          - Use **bold** for emphasis
          - Use bullet points (- item) for lists
          - Use tables where appropriate for comparing data
          - Use markdown for any links: [text](url)
        Please fix your report if you found it isn't in proper markdown format
        
        Do not preface the content with section labels. Write the section as if it's part of a complete report.
        """
        
        try:
            section_content = self._call_llm(prompt)
            return section_content
        except Exception as e:
            return f"Error generating {title} section: {str(e)}"
    
    def compile_full_report(self, report_template: Dict[str, Any], section_contents: Dict[str, str]) -> str:
        """
        Compile all sections into a complete report.
        
        Args:
            report_template (dict): The report template/structure.
            section_contents (dict): The contents of each section.
            
        Returns:
            str: The full report in Markdown format.
        """
        title = report_template.get("title", "Financial Analysis Report")
        date = report_template.get("date", datetime.now().strftime("%B %d, %Y"))
        
        report = f"# {title}\n\n"
        report += f"**Date:** {date}\n\n"
        
        # Add table of contents
        report += "## Table of Contents\n\n"
        for section_name in section_contents.keys():
            section_title = report_template.get("structure", {}).get(section_name, {}).get("title", section_name.replace("_", " ").title())
            report += f"- [{section_title}](#{section_title.lower().replace(' ', '-')})\n"
        
        report += "\n---\n\n"
        
        # Add each section
        for section_name, content in section_contents.items():
            section_title = report_template.get("structure", {}).get(section_name, {}).get("title", section_name.replace("_", " ").title())
            report += f"## {section_title}\n\n"
            report += f"{content}\n\n"
            report += "---\n\n"
        
        # Add disclaimer
        report += """
## Disclaimer

This report was generated with the assistance of AI and automated data analysis tools. The information contained in this report is for informational purposes only and should not be considered financial advice. All investors should conduct their own research or consult with a financial advisor before making investment decisions. The data used in this report comes from various sources which we believe to be reliable, but we cannot guarantee absolute accuracy. Past performance is not indicative of future results.
"""
        
        return report
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data to create a financial research report.
        
        Args:
            input_data (dict): Input data containing analysis results, ticker, company info, etc.
            
        Returns:
            dict: The generated report.
        """
        ticker = input_data.get("ticker", "")
        company_profile = input_data.get("company_profile", [{}])
        research_plan = input_data.get("research_plan", {})
        analysis_results = input_data.get("analysis_results", {})
        
        if not ticker:
            return {"error": "No ticker symbol provided"}
            
        # Extract company info
        if isinstance(company_profile, list) and len(company_profile) > 0:
            company_info = company_profile[0]
        else:
            company_info = company_profile
        
        # Generate report structure
        report_template = self.generate_report_structure(ticker, company_info, research_plan)
        
        # Write each section
        section_contents = {}
        for section_name, section_template in report_template.get("structure", {}).items():
            section_contents[section_name] = self.write_report_section(
                section_name, section_template, analysis_results
            )
        
        # Compile full report in Markdown format
        full_report = self.compile_full_report(report_template, section_contents)
        
        return {
            "report": full_report,
            "sections": section_contents,
            "structure": report_template
        }

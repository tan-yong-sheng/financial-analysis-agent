import json
from typing import Dict, Any, List
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    """Agent responsible for creating research and analysis plans."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial planning specialist that creates detailed research and analysis plans"
        super().__init__(role, "Planning Specialist", base_url=base_url, model_name=model_name)
    
    def create_research_plan(self, ticker: str, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a research plan for a given company.
        
        Args:
            ticker (str): The ticker symbol of the company.
            company_info (dict): Basic company information.
            
        Returns:
            dict: The research plan.
        """
        company_name = company_info.get("companyName", "the company")
        sector = company_info.get("sector", "")
        industry = company_info.get("industry", "")
        
        prompt = f"""
        Create a comprehensive financial research plan for {company_name} ({ticker}), a company in the {sector} sector and {industry} industry.
        
        Company Description: {company_info.get('description', 'No description available')}
        
        Your task is to create a detailed research plan that covers:
        
        1. Key Financial Analysis Areas:
           - Identify the most important financial metrics for this company/industry
           - Specify which statements (income, balance sheet, cash flow) need deepest analysis
           - List specific ratios most relevant to this industry
           
        2. Technical Analysis Requirements:
           - Identify which technical indicators are most relevant
           - Specify time periods for analysis (short-term, medium-term, long-term)
           
        3. Industry Research Needs:
           - List key industry metrics and benchmarks
           - Identify main competitors for comparative analysis
           - Highlight industry-specific factors to research
           
        4. Recent Developments:
           - Suggest specific recent events to research (earnings, management changes, etc.)
           - Identify potential regulatory or macroeconomic factors to consider
           
        5. Report Structure:
           - Outline the recommended structure for the final research report
           - Highlight unique sections needed for this specific company/industry
        
        Format your response as a structured JSON with these main sections. Be specific and tailor your plan to this particular company and industry.
        """
        
        try:
            response = self._call_llm(prompt)
            plan = json.loads(response)
            return plan
        except json.JSONDecodeError:
            # If response isn't valid JSON, return a simplified structure
            return {
                "error": "Failed to create structured plan",
                "raw_plan": response,
                "basic_plan": {
                    "financial_analysis": ["income_statement", "balance_sheet", "cash_flow"],
                    "technical_analysis": ["SMA", "EMA", "RSI"],
                    "industry_research": ["competitors", "industry_trends"],
                    "recent_developments": ["latest_earnings", "news"],
                    "report_structure": ["summary", "financial_analysis", "technical_analysis", "outlook", "recommendation"]
                }
            }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data to create a research plan.
        
        Args:
            input_data (dict): Input data containing ticker and company information.
            
        Returns:
            dict: The research plan.
        """
        ticker = input_data.get("ticker")
        company_info = input_data.get("company_info", {})
        
        if not ticker:
            return {"error": "No ticker symbol provided"}
        
        return self.create_research_plan(ticker, company_info)

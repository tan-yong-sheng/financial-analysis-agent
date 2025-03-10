import sys
import os
import json
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent
from modules.financial_analyzer import FinancialAnalyzer
from tools.data_transformer import NumpyEncoder, convert_numpy_types

class AnalysisAgent(BaseAgent):
    """Agent responsible for analyzing financial data and generating insights."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial analyst that interprets financial data and identifies key trends and insights"
        super().__init__(role, "Financial Analyst", base_url=base_url, model_name=model_name)
        self.analyzer = FinancialAnalyzer()
        
    def analyze_financial_data(self, financial_data: Dict[str, Any], research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze financial data based on the research plan.
        
        Args:
            financial_data (dict): Financial data collected for the company.
            research_plan (dict): The research plan.
            
        Returns:
            dict: Analysis results.
        """
        # Use the existing analyzer module to perform comprehensive analysis
        analysis_results = self.analyzer.comprehensive_analysis(financial_data)
        
        # Extract company information
        company_profile = financial_data.get("company_profile", [{}])
        if isinstance(company_profile, list) and len(company_profile) > 0:
            company_info = company_profile[0]
        else:
            company_info = company_profile
            
        company_name = company_info.get("companyName", "the company")
        sector = company_info.get("sector", "")
        industry = company_info.get("industry", "")
        
        # Ensure analysis_results doesn't have any NumPy types before serializing
        safe_analysis_results = convert_numpy_types(analysis_results)
        
        # Enhance analysis with LLM insights using our custom JSON encoder
        prompt = f"""
        I need you to analyze the financial data for {company_name}, a company in the {sector} sector and {industry} industry.
        
        Here are the key analysis results:
        {json.dumps(safe_analysis_results, cls=NumpyEncoder, indent=2)}
        
        Based on these analysis results and your knowledge of financial analysis:
        
        1. What are the most significant financial trends visible in the data?
        2. How do the key financial ratios compare to industry standards?
        3. What strengths and weaknesses does the financial data reveal?
        4. What specific risks can you identify from the financial data?
        5. Are there any notable anomalies or red flags in the financial statements?
        
        Provide your expert financial analysis in a structured JSON format with clear sections for each area of analysis.
        """
        
        try:
            response = self._call_llm(prompt)
            enhanced_analysis = json.loads(response)
            
            # Combine algorithmic analysis with LLM insights
            complete_analysis = {
                "quantitative_analysis": safe_analysis_results,
                "qualitative_analysis": enhanced_analysis
            }
            
            return complete_analysis
        except json.JSONDecodeError:
            # If LLM response isn't valid JSON, return just the quantitative analysis
            return {
                "quantitative_analysis": safe_analysis_results,
                "error": "Failed to generate enhanced qualitative analysis"
            }
    
    def integrate_market_research(self, analysis_results: Dict[str, Any], research_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate market research with financial analysis.
        
        Args:
            analysis_results (dict): Financial analysis results.
            research_results (dict): Market research results.
            
        Returns:
            dict: Integrated analysis.
        """
        # Convert any NumPy types to native Python types before serialization
        safe_analysis = convert_numpy_types(analysis_results)
        safe_research = convert_numpy_types(research_results)
        
        prompt = f"""
        I have both financial analysis data and market research for a company. Help me integrate these insights.
        
        Financial Analysis:
        {json.dumps(safe_analysis, cls=NumpyEncoder, indent=2)}
        
        Market Research:
        {json.dumps(safe_research, cls=NumpyEncoder, indent=2)}
        
        Please create a comprehensive integrated analysis that:
        
        1. Identifies connections between financial performance and market events/trends
        2. Evaluates how competitive position affects financial results
        3. Assesses how industry trends might impact future financial performance
        4. Determines if financial data aligns with or contradicts market perception
        5. Provides a holistic assessment of the company's position and outlook
        
        Format your response as a detailed JSON with clear sections for each integrated insight area.
        """
        
        try:
            response = self._call_llm(prompt)
            integrated_analysis = json.loads(response)
            
            # Create final integrated analysis
            final_analysis = {
                "financial_analysis": safe_analysis,
                "market_research": safe_research,
                "integrated_insights": integrated_analysis
            }
            
            return final_analysis
        except json.JSONDecodeError:
            return {
                "financial_analysis": safe_analysis,
                "market_research": safe_research,
                "error": "Failed to generate integrated insights"
            }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data to analyze financial information.
        
        Args:
            input_data (dict): Input data containing financial data, research results, and research plan.
            
        Returns:
            dict: Analysis results.
        """
        financial_data = input_data.get("financial_data", {})
        research_results = input_data.get("research_results", {})
        research_plan = input_data.get("research_plan", {})
        
        if not financial_data:
            return {"error": "No financial data provided for analysis"}
        
        # Analyze financial data
        analysis_results = self.analyze_financial_data(financial_data, research_plan)
        
        # Integrate with market research if available
        if research_results:
            return self.integrate_market_research(analysis_results, research_results)
        
        return {"financial_analysis": analysis_results}

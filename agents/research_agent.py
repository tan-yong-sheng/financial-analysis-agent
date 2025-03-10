import sys
import os
import json
from typing import Dict, Any, List
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent
from config import MAX_SEARCH_RESULTS, MAX_RESEARCH_DEPTH
from tools.web_research import WebResearchTool

class ResearchAgent(BaseAgent):
    """Agent responsible for conducting web research and finding relevant information."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial research specialist that gathers relevant market news and industry information"
        super().__init__(role, "Research Specialist", base_url=base_url, model_name=model_name)
        self.research_tool = WebResearchTool()
        
    def web_search(self, query: str, num_results: int = MAX_SEARCH_RESULTS) -> List[Dict[str, Any]]:
        """
        Perform a web search using the web research tool.
        
        Args:
            query (str): The search query.
            num_results (int): Number of results to return.
            
        Returns:
            list: List of search results.
        """
        return self.research_tool.search_google(query, num_results)
    
    def research_company_news(self, ticker: str, company_name: str) -> List[Dict[str, Any]]:
        """
        Research recent news about a company.
        
        Args:
            ticker (str): The ticker symbol.
            company_name (str): The company name.
            
        Returns:
            list: Recent news about the company.
        """
        query = f"{company_name} {ticker} stock news last 3 months"
        # Use news-specific search if available
        try:
            results = self.research_tool.search_news(query)
        except:
            results = self.web_search(query)
        
        # Further process and validate results
        prompt = f"""
        I've conducted a search for news about {company_name} ({ticker}). Here are the results:
        {json.dumps(results, indent=2)}
        
        Please analyze these search results and:
        1. Identify the most relevant and significant news items
        2. Filter out any duplicate or low-quality sources
        3. Add a brief summary of what each news piece is about
        4. Rate each news item's potential impact on the stock (High/Medium/Low)
        
        Return your analysis as a JSON array with each news item containing:
        - title: The title of the news
        - source: The source website
        - url: The URL of the article
        - date: The date of publication (if available)
        - summary: Your brief summary of the article
        - impact: Your assessment of potential impact (High/Medium/Low)
        """
        
        try:
            response = self._call_llm(prompt)
            processed_results = json.loads(response)
            return processed_results
        except json.JSONDecodeError:
            return [{"error": "Failed to process news results", "raw_results": results}]
    
    def research_industry_trends(self, industry: str, sector: str) -> Dict[str, Any]:
        """
        Research industry trends.
        
        Args:
            industry (str): The industry name.
            sector (str): The sector name.
            
        Returns:
            dict: Industry trend information.
        """
        query = f"{industry} {sector} industry trends analysis outlook"
        results = self.web_search(query)
        
        prompt = f"""
        I've conducted a search about trends in the {industry} industry within the {sector} sector. Here are the results:
        {json.dumps(results, indent=2)}
        
        Please analyze these search results and create a comprehensive industry analysis that includes:
        1. Key industry trends and developments
        2. Growth prospects for the industry
        3. Major challenges and risks facing the industry
        4. Competitive landscape
        5. Regulatory environment
        
        Format your response as a detailed JSON with these main sections. Be specific and analytical.
        """
        
        try:
            response = self._call_llm(prompt)
            industry_analysis = json.loads(response)
            return industry_analysis
        except json.JSONDecodeError:
            return {"error": "Failed to process industry research", "raw_results": results}
    
    def research_competitors(self, ticker: str, company_name: str, industry: str) -> Dict[str, Any]:
        """
        Research company competitors.
        
        Args:
            ticker (str): The ticker symbol.
            company_name (str): The company name.
            industry (str): The industry name.
            
        Returns:
            dict: Competitor information.
        """
        query = f"{company_name} {ticker} competitors {industry}"
        results = self.web_search(query)
        
        prompt = f"""
        I've conducted a search about competitors for {company_name} ({ticker}) in the {industry} industry. Here are the results:
        {json.dumps(results, indent=2)}
        
        Please analyze these search results and:
        1. Identify the main direct competitors (ideally with their ticker symbols)
        2. Provide a brief overview of each main competitor
        3. Compare relative market positions (market share, strengths, weaknesses)
        4. Identify any competitive advantages or disadvantages for {company_name}
        
        Format your response as a structured JSON with a "competitors" array and a "competitive_analysis" section.
        """
        
        try:
            response = self._call_llm(prompt)
            competitor_analysis = json.loads(response)
            return competitor_analysis
        except json.JSONDecodeError:
            return {"error": "Failed to process competitor research", "raw_results": results}
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the research request for a company
        
        Args:
            input_data (Dict[str, Any]): Input data containing company information
            
        Returns:
            Dict[str, Any]: Research results
        """
        ticker = input_data.get("ticker")
        company_profile = input_data.get("company_profile", [{}])
        research_plan = input_data.get("research_plan", {})
        
        if not ticker or not company_profile:
            return {"error": "Insufficient information provided"}
        
        # Extract company info
        if isinstance(company_profile, list) and len(company_profile) > 0:
            company_info = company_profile[0]
        else:
            company_info = company_profile
            
        company_name = company_info.get("companyName", "")
        industry = company_info.get("industry", "")
        sector = company_info.get("sector", "")
        
        # Conduct research
        research_results = {
            "company_news": self.research_company_news(ticker, company_name),
            "industry_trends": self.research_industry_trends(industry, sector),
            "competitor_analysis": self.research_competitors(ticker, company_name, industry)
        }
        
        return research_results

import sys
import os
import json
import re
from typing import Dict, Any, List
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from config import MAX_SEARCH_RESULTS, MAX_RESEARCH_DEPTH, SERPAPI_API_KEY
from utils.llm_utils import parse_llm_json_response, parse_and_validate_llm_response, parse_list_response
from models.research_models import ResearchPlan, ArticleContent, SearchResult, ResearchAnalysis, SearchResults
from utils.observability import monitor_agent_method, StructuredLogger, AgentTracer

logger = logging.getLogger(__name__)
structured_logger = StructuredLogger("ResearchAgent")

class ResearchAgent(BaseAgent):
    """Agent responsible for conducting market research and gathering information."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        """Initialize research agent."""
        role = "a financial researcher that conducts market research and gathers information about companies and industries"
        super().__init__(role, "Market Researcher", base_url=base_url, model_name=model_name)
        self.tracer = AgentTracer("Market Researcher", structured_logger)
    
    @monitor_agent_method()
    def create_research_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.tracer.start_task("create_research_plan", ticker=input_data.get("ticker"))
        try:
            ticker = input_data.get("ticker")
            company_data = input_data.get("company_data", {})
            
            if not ticker:
                return {"error": "No ticker symbol provided for research planning"}
                
            # Get company information from the data if available
            company_name = company_data.get("companyName", ticker)
            company_sector = company_data.get("sector", "")
            company_industry = company_data.get("industry", "")
            company_description = company_data.get("description", "")
                
            # Generate research plan with LLM using structured output
            prompt = f"""
            Create a detailed financial research plan for {company_name} ({ticker}).

            Company Details:
            - Sector: {company_sector}
            - Industry: {company_industry}
            - Description: {company_description}

            Include key financial metrics to analyze, specific industry factors to research, 
            main competitors to compare against, market trends to investigate,
            potential risks and opportunities to identify, and recent news and events to research.

            For each area, provide specific questions that should be answered during research.
            """
            
            try:
                # Use structured output with instructor
                plan = self._call_structured_llm(prompt, ResearchPlan)
                
                # Ensure ticker and company name are included
                plan.ticker = ticker
                plan.company_name = company_name
                
                # Convert to dictionary for compatibility with existing code
                result = plan.model_dump()
                self.tracer.end_task(status="success", result_summary={"ticker": result.get("ticker")})
                return result
                
            except Exception as e:
                logger.error(f"Error creating research plan: {str(e)}")
                self.tracer.end_task(status="error", error_message=str(e))
                return {
                    "ticker": ticker,
                    "company_name": company_name,
                    "key_areas": ["financial_performance", "market_position", "industry_trends", "risks"],
                    "metrics": ["revenue_growth", "profit_margins", "debt_to_equity", "return_on_equity"],
                    "competitors": [],
                    "industry_factors": [],
                    "questions": ["What is the company's financial health?", 
                                "How does it compare to competitors?",
                                "What are the key risks and opportunities?"],
                    "research_sources": ["financial_statements", "news_articles", "analyst_reports"]
                }
        except Exception as e:
            self.tracer.end_task(status="error", error_message=str(e))
            raise

    def search_web(self, query: str, num_results: int = MAX_SEARCH_RESULTS) -> List[Dict[str, Any]]:
        """
        Search the web for information using SerpAPI.
        
        Args:
            query (str): Search query
            num_results (int): Maximum number of results to return
            
        Returns:
            list: Search results
        """
        # In a real implementation, this would use SerpAPI
        # For now, simulate a response with structured information
        prompt = f"""
        Generate {num_results} realistic search results for the query: "{query}"
        
        Each result should include title, link, and snippet that would be helpful for financial analysis.
        Make sure the information is factually plausible.
        """
        
        try:
            # Use instructor for structured output
            results = self._call_structured_llm(prompt, SearchResults)
            
            # Take only the requested number
            results_list = results.results[:num_results]
            
            # Convert to dict
            return [item.model_dump() for item in results_list]
            
        except Exception as e:
            logger.error(f"Error in search_web: {str(e)}")
            return [{"error": f"Failed to get search results: {str(e)}"}]

    def extract_article_content(self, url: str) -> Dict[str, Any]:
        """
        Extract and summarize content from a URL.
        
        Args:
            url (str): The URL to extract content from
            
        Returns:
            dict: Extracted content and summary
        """
        # Simulate content extraction with structured output
        prompt = f"""
        Extract content from the URL: {url}
        
        Based on the URL, generate realistic but fictional article content that might
        appear on this page, focusing on financial/business information.
        Include a title, publication date, content paragraphs, and a concise 2-3 sentence summary.
        """
        
        try:
            # Use instructor for structured output
            content = self._call_structured_llm(prompt, ArticleContent)
            
            # Convert to dict
            return content.model_dump()
            
        except Exception as e:
            logger.error(f"Error extracting article content: {str(e)}")
            return {"error": f"Failed to extract content: {str(e)}"}

    def conduct_research(self, research_plan: Dict[str, Any], depth: int = MAX_RESEARCH_DEPTH) -> Dict[str, Any]:
        """
        Conduct research based on the research plan.
        
        Args:
            research_plan (dict): Research plan with focus areas and questions
            depth (int): Maximum depth of research to conduct
            
        Returns:
            dict: Research findings
        """
        ticker = research_plan.get("ticker")
        company_name = research_plan.get("company_name", ticker)
        
        # Initialize research findings
        findings = {
            "company_overview": {},
            "financial_insights": [],
            "market_position": {},
            "industry_analysis": {},
            "news_and_events": [],
            "risk_factors": []
        }
        
        # Get company overview
        company_query = f"{company_name} {ticker} company overview financial"
        company_results = self.search_web(company_query, 3)
        if company_results and isinstance(company_results[0], dict) and "error" not in company_results[0]:
            findings["company_overview"] = self.extract_article_content(company_results[0]["link"])
        
        # Research recent financial performance
        financial_query = f"{company_name} {ticker} recent financial performance quarterly results"
        financial_results = self.search_web(financial_query, 5)
        for result in financial_results[:depth]:
            if isinstance(result, dict) and "link" in result:
                article = self.extract_article_content(result["link"])
                if "error" not in article:
                    findings["financial_insights"].append(article)
        
        # Research industry trends
        industry = research_plan.get("industry", "")
        industry_query = f"{industry} industry trends market analysis {company_name}"
        industry_results = self.search_web(industry_query, 3)
        if industry_results and isinstance(industry_results[0], dict) and "link" in industry_results[0]:
            findings["industry_analysis"] = self.extract_article_content(industry_results[0]["link"])
        
        # Get recent news
        news_query = f"{company_name} {ticker} recent news events last 3 months"
        news_results = self.search_web(news_query, 5)
        for result in news_results[:depth]:
            if isinstance(result, dict) and "link" in result:
                article = self.extract_article_content(result["link"])
                if "error" not in article:
                    findings["news_and_events"].append(article)
        
        # Research competitors
        competitors = research_plan.get("competitors", [])
        if competitors:
            competitors_str = ", ".join(competitors)
            comp_query = f"{company_name} vs {competitors_str} market comparison"
            comp_results = self.search_web(comp_query, 2)
            if comp_results and isinstance(comp_results[0], dict) and "link" in comp_results[0]:
                findings["market_position"] = self.extract_article_content(comp_results[0]["link"])
                
        return findings
        
    def analyze_research_findings(self, research_findings: Dict[str, Any], research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze research findings to extract key insights.
        
        Args:
            research_findings (dict): Raw research findings
            research_plan (dict): Original research plan
            
        Returns:
            dict: Analyzed research findings with key insights
        """
        ticker = research_plan.get("ticker")
        company_name = research_plan.get("company_name", ticker)
        
        # Prepare content for LLM analysis
        prompt = f"""
        Analyze research findings for {company_name} ({ticker}) to extract key insights.
        
        Research Plan:
        {json.dumps(research_plan, indent=2)}
        
        Research Findings:
        {json.dumps(research_findings, indent=2)}
        
        Extract:
        1. Key market trends affecting the company
        2. Competitive position analysis
        3. Major risks and opportunities
        4. Recent events that may impact financial performance
        5. Industry outlook and how it affects the company
        
        Include citations to the source material when possible.
        """
        
        try:
            # Use instructor for structured output
            analysis = self._call_structured_llm(prompt, ResearchAnalysis)
            
            # Combine with original findings for a complete research package
            return {
                "ticker": ticker,
                "company_name": company_name,
                "raw_findings": research_findings,
                "analysis": analysis.model_dump()
            }
            
        except Exception as e:
            logger.error(f"Error parsing research analysis: {str(e)}")
            return {
                "ticker": ticker,
                "company_name": company_name,
                "raw_findings": research_findings,
                "error": f"Failed to analyze research findings: {str(e)}"
            }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data to conduct market research.
        
        Args:
            input_data (dict): Input data containing ticker, company data, and research plan.
            
        Returns:
            dict: Research results.
        """
        ticker = input_data.get("ticker")
        company_data = input_data.get("company_data", {})
        research_plan = input_data.get("research_plan", {})
        
        if not ticker:
            return {"error": "No ticker provided for research"}
            
        # If no research plan provided, create one
        if not research_plan or "error" in research_plan:
            research_plan = self.create_research_plan({
                "ticker": ticker,
                "company_data": company_data
            })
            
        # Conduct research based on plan
        research_findings = self.conduct_research(research_plan)
        
        # Analyze findings
        return self.analyze_research_findings(research_findings, research_plan)

import os
import json
from typing import Dict, Any, List, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our search client
from utils.search import SearchClient

logger = logging.getLogger("Web_Research_Tool")

class WebResearchTool:
    """Tool for conducting web research using search APIs."""
    
    def __init__(self):
        """Initialize the web research tool."""
        self.search_client = SearchClient()
        
    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Perform a Google search query.
        
        Args:
            query (str): Search query
            num_results (int): Number of results to return
            
        Returns:
            list: Search results
        """
        try:
            search_results = self.search_client.search(query, num=num_results)
            
            # Extract organic results from the search response
            organic_results = search_results.get("organic_results", [])
            if not organic_results:
                return [{"error": "No organic results found in search response"}]
                
            # Format the results
            formatted_results = []
            for result in organic_results[:num_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "source": result.get("source", "")
                })
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in search_google: {str(e)}")
            return [{"error": f"Search error: {str(e)}"}]
    
    def search_news(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for news articles.
        
        Args:
            query (str): Search query
            num_results (int): Number of results to return
            
        Returns:
            list: News search results
        """
        try:
            news_results = self.search_client.get_news(query)
            
            # Handle the case where news_results might be a string
            if isinstance(news_results, str):
                logger.warning("Received string response instead of dict in search_news")
                return [{"error": "Invalid response format from news search", "raw": news_results[:200]}]
            
            # Extract news results
            news_items = news_results.get("news_results", [])
            if not news_items and "organic_results" in news_results:
                # Fall back to organic results if no specific news results
                news_items = news_results.get("organic_results", [])
            
            if not news_items:
                return [{"error": "No news results found in search response"}]
                
            # Format the results
            formatted_results = []
            for item in news_items[:num_results]:
                # Extract source name handling different possible formats
                source = ""
                if isinstance(item.get("source"), dict):
                    source = item.get("source", {}).get("name", "")
                elif isinstance(item.get("source"), str):
                    source = item.get("source", "")
                
                formatted_results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": source,
                    "date": item.get("date", "")
                })
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in search_news: {str(e)}")
            return [{"error": f"News search error: {str(e)}"}]
    
    def get_company_competitors(self, company: str, industry: str) -> List[Dict[str, Any]]:
        """
        Find competitors for a company.
        
        Args:
            company (str): Company name
            industry (str): Industry name
            
        Returns:
            list: Competitor information
        """
        query = f"{company} competitors in {industry} industry"
        return self.search_google(query)
    
    def get_industry_trends(self, industry: str) -> List[Dict[str, Any]]:
        """
        Research industry trends.
        
        Args:
            industry (str): Industry name
            
        Returns:
            list: Industry trends information
        """
        query = f"{industry} industry trends analysis 2023"
        return self.search_google(query)

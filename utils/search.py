import os
import requests
from typing import Dict, Any, Optional

class SearchClient:
    """Client for making search API requests"""
    
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_API_KEY')
        self.base_url = "https://serpapi.com/search"
        
    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Perform a search query using SerpApi
        
        Args:
            query (str): Search query
            **kwargs: Additional search parameters
            
        Returns:
            Dict[str, Any]: Search results
        """
        params = {
            "api_key": self.api_key,
            "q": query,
            "engine": "google",
            **kwargs
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_news(self, query: str, **kwargs) -> Dict[str, Any]:
        """Get news results for a query"""
        return self.search(query, tbm="nws", **kwargs)
    
    def get_company_info(self, company: str) -> Dict[str, Any]:
        """Get company-specific search results"""
        return self.search(f"{company} company information", num=10)

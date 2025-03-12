"""
Test script for web search functionality.
This script demonstrates both simulated search and actual SerpAPI search.
"""

import sys
import os
import json
import logging
from typing import Dict, Any, List
import argparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary components
from agents.research_agent import ResearchAgent
from config import SERPAPI_API_KEY

def test_simulated_search(query: str, num_results: int = 3) -> None:
    """Test the simulated search using LLM."""
    logger.info(f"Testing simulated search for: {query}")
    
    # Initialize the research agent
    agent = ResearchAgent()
    
    # Use the existing search_web method (which is simulation-based)
    results = agent.search_web(query, num_results)
    
    # Print the results
    logger.info(f"Found {len(results)} simulated results:")
    for i, result in enumerate(results, 1):
        logger.info(f"\nResult {i}:")
        logger.info(f"Title: {result.get('title', 'N/A')}")
        logger.info(f"Link: {result.get('link', 'N/A')}")
        logger.info(f"Snippet: {result.get('snippet', 'N/A')[:100]}...")
    
    return results

def test_actual_serpapi_search(query: str, num_results: int = 3) -> List[Dict[str, Any]]:
    """Test actual SerpAPI search using direct REST API calls."""
    logger.info(f"Testing actual SerpAPI search for: {query}")
    
    try:
        import requests
        
        # Validate API key
        if not SERPAPI_API_KEY:
            logger.error("No SerpAPI key provided. Please add it to your config.")
            return [{"error": "No SerpAPI key configured"}]
        
        # Set up the search parameters
        base_url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
            "num": num_results,
            "gl": "us"  # Country to use for the search
        }
        
        # Execute the search
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        results = response.json()
        
        # Process the organic results
        organic_results = results.get("organic_results", [])
        
        # Format the results similar to the simulation for consistency
        formatted_results = []
        for i, result in enumerate(organic_results[:num_results], 1):
            formatted_result = {
                "title": result.get("title", ""),
                "link": result.get("link", ""),
                "snippet": result.get("snippet", ""),
                "_source": {
                    "type": "web_search",
                    "query": query,
                    "search_date": ResearchAgent()._get_current_date(),
                    "result_position": i,
                    "search_engine": "SerpAPI (actual)"
                }
            }
            formatted_results.append(formatted_result)
        
        # Print the results
        logger.info(f"Found {len(formatted_results)} actual search results:")
        for i, result in enumerate(formatted_results, 1):
            logger.info(f"\nResult {i}:")
            logger.info(f"Title: {result.get('title', 'N/A')}")
            logger.info(f"Link: {result.get('link', 'N/A')}")
            logger.info(f"Snippet: {result.get('snippet', 'N/A')[:100]}...")
        
        return formatted_results
        
    except ImportError as e:
        logger.error(f"Required library not installed: {str(e)}")
        return [{"error": f"Required library not installed: {str(e)}"}]
        
    except Exception as e:
        logger.error(f"Error performing SerpAPI search: {str(e)}")
        return [{"error": f"Failed to get search results: {str(e)}"}]

def main():
    """Main function to test web search functionality."""
    parser = argparse.ArgumentParser(description="Test web search functionality")
    parser.add_argument("query", nargs="?", default="Apple Inc financial performance", 
                        help="Search query to test")
    parser.add_argument("--num-results", type=int, default=3,
                        help="Number of search results to return")
    parser.add_argument("--mode", choices=["simulated", "actual", "both"], default="both",
                        help="Search mode: simulated, actual, or both")
    
    args = parser.parse_args()
    
    if args.mode in ["simulated", "both"]:
        sim_results = test_simulated_search(args.query, args.num_results)
    
    if args.mode in ["actual", "both"]:
        api_results = test_actual_serpapi_search(args.query, args.num_results)
    
    logger.info("Search testing complete")

if __name__ == "__main__":
    main()

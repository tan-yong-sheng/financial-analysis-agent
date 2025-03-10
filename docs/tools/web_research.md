# Web Research Tool

The Web Research Tool enables the system to gather information from the web using search APIs. It's primarily used by the Research Agent to find news, articles, and other information about companies, industries, and market trends.

## Overview

The Web Research Tool simplifies the process of searching for and collecting information from the web. It provides a consistent interface for performing searches, processing results, and extracting relevant information.

## Implementation

```python
class WebResearchTool:
    """Tool for conducting web research using search APIs."""
    
    def __init__(self):
        """Initialize the web research tool."""
        self.search_client = SearchClient()
        
    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Perform a Google search query."""
        # Implementation details...
    
    def search_news(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search for news articles."""
        # Implementation details...
    
    def get_company_competitors(self, company: str, industry: str) -> List[Dict[str, Any]]:
        """Find competitors for a company."""
        # Implementation details...
    
    def get_industry_trends(self, industry: str) -> List[Dict[str, Any]]:
        """Research industry trends."""
        # Implementation details...
```

## Key Features

### General Web Search

The `search_google` method performs general web searches:

```python
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
```

### News Search

The `search_news` method is specialized for finding news articles:

```python
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
        
        # Extract news results
        news_items = news_results.get("news_results", [])
        if not news_items:
            return [{"error": "No news results found in search response"}]
            
        # Format the results
        formatted_results = []
        for item in news_items[:num_results]:
            formatted_results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": item.get("source", {}).get("name", ""),
                "date": item.get("date", "")
            })
            
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error in search_news: {str(e)}")
        return [{"error": f"News search error: {str(e)}"}]
```

### Specialized Research Methods

The tool also provides methods for specific research tasks:

1. **Competitor Research**: Find competitors for a specific company
2. **Industry Trends**: Research trends within a particular industry 

These specialized methods build on the base search functionality but construct specific queries and process the results accordingly.

## Search Client Integration

The Web Research Tool uses a `SearchClient` class that wraps the actual search API (currently SerpAPI):

```python
class SearchClient:
    """Client for making search API requests"""
    
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_API_KEY')
        self.base_url = "https://serpapi.com/search"
        
    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Perform a search query using SerpApi"""
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
```

This design allows for easy switching to different search providers in the future.

## Error Handling

The Web Research Tool includes robust error handling:

1. **Network Errors**: Connection issues are caught and formatted as error objects
2. **API Errors**: Errors from the search API are properly logged
3. **Empty Results**: Cases where no results are found are handled gracefully
4. **Parsing Errors**: Issues with processing search results are caught

All errors are logged and returned as structured objects:

```json
[{"error": "Search error: API rate limit exceeded"}]
```

## Example Usage

```python
from tools.web_research import WebResearchTool

# Initialize the tool
research_tool = WebResearchTool()

# Perform a general search
results = research_tool.search_google("Apple financial performance 2023")

# Check for errors
if results and "error" in results[0]:
    print(f"Search error: {results[0]['error']}")
else:
    # Process the results
    for result in results:
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Snippet: {result['snippet']}\n")

# Search for news
news = research_tool.search_news("Apple earnings Q1 2023")
for article in news:
    print(f"{article.get('title')} - {article.get('source')}")
```

## Search API Limitations

Using search APIs like SerpAPI has some limitations:

1. **Cost**: Search APIs typically charge per request
2. **Rate Limits**: Most APIs impose request rate limitations
3. **Freshness**: Results may not always include the very latest information
4. **Content Restrictions**: Some content may not be indexed or accessible

The Web Research Tool is designed to work within these constraints by:
- Limiting the number of results returned by default
- Providing focused search methods to get relevant results
- Handling rate limiting errors gracefully
- Processing results to extract the most relevant information

## Future Enhancements

Potential improvements to the Web Research Tool include:

1. **Content Extraction**: Retrieving and parsing the full content of articles
2. **Multiple Search Engines**: Using multiple search providers for more comprehensive results
3. **Cached Results**: Implementing caching to reduce duplicate API calls
4. **Result Ranking**: Implementing custom relevance ranking beyond what the search API provides
5. **Content Classification**: Automatically categorizing search results by topic or relevance

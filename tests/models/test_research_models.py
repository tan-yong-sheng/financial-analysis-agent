import pytest
from pydantic import ValidationError
from models.research_models import SearchResult, SearchResults, ArticleContent, ResearchPlan, ResearchAnalysis, RisksOpportunities

def test_search_result_model():
    """Test SearchResult model validation"""
    # Valid data
    data = {
        "title": "Test Result",
        "link": "https://example.com",
        "snippet": "Test snippet text"
    }
    result = SearchResult(**data)
    assert result.title == "Test Result"
    assert result.link == "https://example.com"
    
    # Invalid data
    with pytest.raises(ValidationError):
        SearchResult(title="Test", snippet="Missing link field")

def test_search_results_model():
    """Test SearchResults model validation"""
    # Valid data
    data = {
        "results": [
            {
                "title": "Result 1",
                "link": "https://example1.com",
                "snippet": "Snippet 1"
            },
            {
                "title": "Result 2",
                "link": "https://example2.com",
                "snippet": "Snippet 2"
            }
        ]
    }
    results = SearchResults(**data)
    assert len(results.results) == 2
    assert results.results[0].title == "Result 1"
    
    # Empty results should be valid
    empty_results = SearchResults()
    assert len(empty_results.results) == 0

def test_article_content_model():
    """Test ArticleContent model validation"""
    # Valid data
    data = {
        "title": "Test Article",
        "date_published": "2023-01-01",
        "content": "This is article content.",
        "summary": "Article summary."
    }
    article = ArticleContent(**data)
    assert article.title == "Test Article"
    assert article.summary == "Article summary."
    
    # Invalid data
    with pytest.raises(ValidationError):
        ArticleContent(
            title="Missing fields",
            date_published="2023-01-01"
        )

def test_research_plan_model():
    """Test ResearchPlan model validation"""
    # Valid minimal data
    data = {
        "ticker": "AAPL",
        "company_name": "Apple Inc."
    }
    plan = ResearchPlan(**data)
    assert plan.ticker == "AAPL"
    assert plan.company_name == "Apple Inc."
    assert len(plan.key_areas) == 0  # Default empty list
    
    # Valid full data
    full_data = {
        "ticker": "MSFT",
        "company_name": "Microsoft",
        "key_areas": ["financials", "market position"],
        "metrics": ["revenue", "profit margin"],
        "competitors": ["AAPL", "GOOG"],
        "industry_factors": ["cloud computing growth"],
        "questions": ["How profitable is the company?"],
        "research_sources": ["SEC filings", "news articles"]
    }
    full_plan = ResearchPlan(**full_data)
    assert full_plan.ticker == "MSFT"
    assert len(full_plan.key_areas) == 2
    assert len(full_plan.competitors) == 2

def test_research_analysis_model():
    """Test ResearchAnalysis model validation"""
    # Valid data
    data = {
        "market_trends": [
            {"content": "Trend 1", "citation": "Source 1"},
            {"content": "Trend 2", "citation": "Source 2"}
        ],
        "competitive_position": [
            {"content": "Strong market position", "citation": "Source 3"}
        ],
        "risks_opportunities": {
            "risks": [{"content": "Risk 1", "citation": "Source 4"}],
            "opportunities": [{"content": "Opportunity 1", "citation": "Source 5"}]
        },
        "recent_events": [
            {"content": "Product launch", "citation": "Source 6"},
            {"content": "Acquisition", "citation": "Source 7"}
        ],
        "industry_outlook": {"content": "Positive growth expected", "citation": "Source 8"}
    }
    analysis = ResearchAnalysis(**data)
    
    # Verify structure
    assert len(analysis.market_trends) == 2
    assert analysis.market_trends[0].content == "Trend 1"
    assert analysis.market_trends[0].citation == "Source 1"
    assert len(analysis.competitive_position) == 1
    assert analysis.competitive_position[0].content == "Strong market position"
    assert analysis.risks_opportunities.risks[0].content == "Risk 1"
    assert analysis.industry_outlook.content == "Positive growth expected"

    # Default values for risks_opportunities
    minimal_data = {
        "competitive_position": "Average",
        "industry_outlook": "Stable"
    }
    min_analysis = ResearchAnalysis(**minimal_data)
    assert len(min_analysis.market_trends) == 0
    assert len(min_analysis.risks_opportunities.risks) == 0
    assert len(min_analysis.risks_opportunities.opportunities) == 0

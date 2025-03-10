import pytest
from unittest.mock import MagicMock, patch
from agents.research_agent import ResearchAgent
from models.research_models import SearchResults, SearchResult, ArticleContent, ResearchPlan, ResearchAnalysis

@pytest.fixture
def mock_research_agent():
    with patch('agents.research_agent.ResearchAgent._call_structured_llm') as mock_call:
        agent = ResearchAgent()
        agent._call_structured_llm = mock_call
        yield agent, mock_call

def test_create_research_plan(mock_research_agent):
    """Test create_research_plan uses structured output"""
    agent, mock_call = mock_research_agent
    
    # Setup mock
    plan = ResearchPlan(
        ticker="AAPL",
        company_name="Apple Inc.",
        key_areas=["financials", "competitors"],
        metrics=["revenue", "profit"],
        competitors=["MSFT", "GOOG"],
        questions=["How profitable is the company?"]
    )
    mock_call.return_value = plan
    
    # Execute
    result = agent.create_research_plan({"ticker": "AAPL"})
    
    # Assert
    mock_call.assert_called_once()
    assert mock_call.call_args[0][1] == ResearchPlan
    assert result["ticker"] == "AAPL"
    assert "key_areas" in result
    assert "metrics" in result
    assert "competitors" in result

def test_search_web(mock_research_agent):
    """Test search_web method with structured output"""
    agent, mock_call = mock_research_agent
    
    # Setup mock
    search_results = SearchResults(results=[
        SearchResult(title="Test Result", link="https://test.com", snippet="Test snippet"),
        SearchResult(title="Another Result", link="https://example.com", snippet="Example snippet")
    ])
    mock_call.return_value = search_results
    
    # Execute
    results = agent.search_web("test query", 2)
    
    # Assert
    mock_call.assert_called_once()
    assert mock_call.call_args[0][1] == SearchResults
    assert len(results) == 2
    assert results[0]["title"] == "Test Result"
    assert results[1]["link"] == "https://example.com"

def test_extract_article_content(mock_research_agent):
    """Test extract_article_content with structured output"""
    agent, mock_call = mock_research_agent
    
    # Setup mock
    content = ArticleContent(
        title="Test Article",
        date_published="2023-01-01",
        content="Article content here",
        summary="Article summary"
    )
    mock_call.return_value = content
    
    # Execute
    result = agent.extract_article_content("https://test.com")
    
    # Assert
    mock_call.assert_called_once()
    assert mock_call.call_args[0][1] == ArticleContent
    assert result["title"] == "Test Article"
    assert result["content"] == "Article content here"

def test_analyze_research_findings(mock_research_agent):
    """Test analyze_research_findings with structured output"""
    agent, mock_call = mock_research_agent
    
    # Setup mock
    analysis = ResearchAnalysis(
        market_trends=["Trend 1", "Trend 2"],
        competitive_position="Strong position",
        risks_opportunities={
            "risks": ["Risk 1"],
            "opportunities": ["Opportunity 1"]
        },
        recent_events=["Event 1"],
        industry_outlook="Positive outlook"
    )
    mock_call.return_value = analysis
    
    # Execute
    research_plan = {"ticker": "AAPL", "company_name": "Apple Inc."}
    research_findings = {"company_overview": {}, "financial_insights": []}
    result = agent.analyze_research_findings(research_findings, research_plan)
    
    # Assert
    mock_call.assert_called_once()
    assert mock_call.call_args[0][1] == ResearchAnalysis
    assert result["ticker"] == "AAPL"
    assert "analysis" in result
    assert result["analysis"]["market_trends"] == ["Trend 1", "Trend 2"]

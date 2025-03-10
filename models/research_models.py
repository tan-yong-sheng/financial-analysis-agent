from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class SearchResult(BaseModel):
    """Model for search engine result"""
    title: str = Field(description="Title of the search result")
    link: str = Field(description="URL of the search result")
    snippet: str = Field(description="Short text excerpt from the search result")

class SearchResults(BaseModel):
    """Container for search results"""
    results: List[SearchResult] = Field(description="List of search results", default_factory=list)

class ArticleContent(BaseModel):
    """Model for extracted article content"""
    title: str = Field(description="Article title")
    date_published: str = Field(description="Publication date of the article")
    content: str = Field(description="Main content of the article")
    summary: str = Field(description="Brief summary of the article content")

class ResearchPlan(BaseModel):
    """Model for research plan created by the research agent"""
    ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Name of the company")
    key_areas: List[str] = Field(description="List of research focus areas", 
                               default_factory=list)
    metrics: List[str] = Field(description="List of important financial metrics to analyze", 
                            default_factory=list)
    competitors: List[str] = Field(description="List of main competitors to research", 
                                default_factory=list)
    industry_factors: List[str] = Field(description="List of industry-specific factors to investigate", 
                                     default_factory=list)
    questions: List[str] = Field(description="List of key questions for the research to answer", 
                              default_factory=list)
    research_sources: List[str] = Field(description="List of recommended data sources for the research", 
                                     default_factory=list)

class RisksOpportunities(BaseModel):
    """Model for risks and opportunities section of research analysis"""
    risks: List[str] = Field(description="List of identified risks", 
                          default_factory=list)
    opportunities: List[str] = Field(description="List of identified opportunities", 
                                  default_factory=list)

class ResearchAnalysis(BaseModel):
    """Model for the analysis of research findings"""
    market_trends: List[str] = Field(description="Key market trends affecting the company", 
                                  default_factory=list)
    competitive_position: str = Field(description="Analysis of company's competitive position")
    risks_opportunities: RisksOpportunities = Field(
        description="Major risks and opportunities", 
        default_factory=lambda: RisksOpportunities(risks=[], opportunities=[])
    )
    recent_events: List[str] = Field(description="Recent events that may impact performance", 
                                  default_factory=list)
    industry_outlook: str = Field(description="Industry outlook and its effect on the company")

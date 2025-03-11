"""
Test script for the AnalysisAgent.
This script demonstrates how to use the analysis agent to analyze financial data
and generate insights.
"""

import sys
import os
import json
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import agents
from agents.data_collection_agent import DataCollectionAgent
try:
    from agents.analysis_agent import AnalysisAgent
except ImportError:
    logger.warning("AnalysisAgent not found. Simulating with a mock implementation.")
    
    class AnalysisAgent:
        """Mock analysis agent for testing purposes."""
        def __init__(self, *args, **kwargs):
            pass
            
        def analyze_financial_data(self, data, analysis_type=None):
            """Mock analysis method."""
            return {
                "analysis_summary": "Mock analysis summary",
                "financial_health": "stable",
                "growth_metrics": {
                    "revenue_growth": "10%",
                    "profit_growth": "8%"
                },
                "key_insights": [
                    "This is a mock analysis",
                    "Replace with actual AnalysisAgent implementation"
                ]
            }


def test_basic_analysis(analysis_agent, financial_data: Dict[str, Any]) -> None:
    """Test basic financial analysis functionality."""
    logger.info("Testing basic financial analysis")
    
    analysis_result = analysis_agent.analyze_financial_data(financial_data)
    
    logger.info(f"Analysis summary: {analysis_result.get('analysis_summary', 'N/A')}")
    logger.info(f"Financial health: {analysis_result.get('financial_health', 'N/A')}")
    
    # Log key insights
    key_insights = analysis_result.get('key_insights', [])
    logger.info(f"Number of insights: {len(key_insights)}")
    for i, insight in enumerate(key_insights[:3]):  # Show first 3 insights
        logger.info(f"Insight {i+1}: {insight}")


def main() -> None:
    """Main function to test the analysis agent."""
    ticker = "AAPL"  # Default ticker
    
    # Allow command line argument for ticker
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    
    logger.info(f"Testing AnalysisAgent with ticker: {ticker}")
    
    # First, collect financial data using DataCollectionAgent
    data_agent = DataCollectionAgent()
    financial_data = data_agent.collect_financial_data(ticker)
    
    # Now initialize and test analysis agent
    analysis_agent = AnalysisAgent()
    test_basic_analysis(analysis_agent, financial_data)


if __name__ == "__main__":
    main()

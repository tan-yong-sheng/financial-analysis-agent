"""
Test script for the DataCollectionAgent.
This script demonstrates how to use the data collection agent to fetch financial data
for a given stock ticker.
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

from agents.data_collection_agent import DataCollectionAgent


def test_company_profile(agent: DataCollectionAgent, ticker: str) -> None:
    """Test fetching company profile."""
    logger.info(f"Testing company profile for {ticker}")
    profile = agent.get_company_profile(ticker)
    logger.info(f"Company name: {profile.get('companyName', 'N/A')}")
    logger.info(f"Industry: {profile.get('industry', 'N/A')}")
    logger.info(f"Market Cap: {profile.get('mktCap', 'N/A')}")


def test_financial_statements(agent: DataCollectionAgent, ticker: str) -> None:
    """Test fetching financial statements."""
    logger.info(f"Testing financial statements for {ticker}")
    
    # Test income statement
    income = agent.get_income_statement(ticker)
    if income and not isinstance(income, dict) and len(income) > 0:
        logger.info(f"Income Statement: {len(income)} periods retrieved")
        logger.info(f"Latest period revenue: {income[0].get('revenue', 'N/A')}")
    else:
        logger.error("Failed to retrieve income statement data")
    
    # Test balance sheet
    balance = agent.get_balance_sheet(ticker)
    if balance and not isinstance(balance, dict) and len(balance) > 0:
        logger.info(f"Balance Sheet: {len(balance)} periods retrieved")
        logger.info(f"Latest period total assets: {balance[0].get('totalAssets', 'N/A')}")
    else:
        logger.error("Failed to retrieve balance sheet data")
    
    # Test cash flow
    cash_flow = agent.get_cash_flow(ticker)
    if cash_flow and not isinstance(cash_flow, dict) and len(cash_flow) > 0:
        logger.info(f"Cash Flow: {len(cash_flow)} periods retrieved")
        logger.info(f"Latest period operating cash flow: {cash_flow[0].get('operatingCashFlow', 'N/A')}")
    else:
        logger.error("Failed to retrieve cash flow data")


def test_technical_indicators(agent: DataCollectionAgent, ticker: str) -> None:
    """Test fetching technical indicators."""
    logger.info(f"Testing technical indicators for {ticker}")
    
    # Test RSI indicator
    rsi = agent.get_technical_indicators(ticker, "rsi")
    logger.info(f"RSI data: {json.dumps(rsi, indent=2)[:200]}...")
    
    # Test all indicators
    all_indicators = agent.get_technical_indicators(ticker)
    for indicator, data in all_indicators.items():
        logger.info(f"Indicator: {indicator}, Data available: {'historical' in data}")


def test_comprehensive_data_collection(agent: DataCollectionAgent, ticker: str) -> None:
    """Test the comprehensive data collection method."""
    logger.info(f"Testing comprehensive data collection for {ticker}")
    data = agent.collect_financial_data(ticker)
    
    # Log some key information
    logger.info(f"Company: {data['company_profile'].get('companyName', 'N/A')}")
    logger.info(f"Number of income statement periods: {len(data['income_statement']) if isinstance(data['income_statement'], list) else 'N/A'}")
    logger.info(f"Number of technical indicators: {len(data['technical_indicators']) if isinstance(data['technical_indicators'], dict) else 'N/A'}")


def main() -> None:
    """Main function to test the data collection agent."""
    ticker = "AAPL"  # Default ticker
    
    # Allow command line argument for ticker
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    
    logger.info(f"Testing DataCollectionAgent with ticker: {ticker}")
    
    # Initialize agent
    agent = DataCollectionAgent()
    
    # Run tests
    test_company_profile(agent, ticker)
    test_financial_statements(agent, ticker)
    test_technical_indicators(agent, ticker)
    test_comprehensive_data_collection(agent, ticker)


if __name__ == "__main__":
    main()

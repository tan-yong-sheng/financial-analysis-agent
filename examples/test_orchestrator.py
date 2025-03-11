"""
Test script for the FinancialAnalysisOrchestrator.
This script demonstrates the end-to-end workflow of the financial analysis system.
"""

import sys
import os
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

try:
    from orchestrator import FinancialAnalysisOrchestrator
except ImportError:
    logger.error("FinancialAnalysisOrchestrator not found.")
    sys.exit(1)


def test_end_to_end_analysis(ticker: str) -> None:
    """Test the entire financial analysis workflow."""
    logger.info(f"Starting end-to-end financial analysis for {ticker}")
    
    try:
        # Initialize the orchestrator
        orchestrator = FinancialAnalysisOrchestrator()
        
        # Run the analysis
        result = orchestrator.run_analysis(ticker)
        
        # Log results
        logger.info(f"Analysis completed for {ticker}")
        logger.info(f"Report summary: {result.get('summary', 'N/A')}")
        
        # Check if a report was generated
        report = result.get('report', {})
        if report:
            logger.info(f"Report sections: {', '.join(report.keys())}")
        else:
            logger.warning("No detailed report generated")
            
    except Exception as e:
        logger.error(f"Error in financial analysis: {str(e)}")


def main() -> None:
    """Main function to test the orchestrator."""
    ticker = "AAPL"  # Default ticker
    
    # Allow command line argument for ticker
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    
    logger.info(f"Testing FinancialAnalysisOrchestrator with ticker: {ticker}")
    test_end_to_end_analysis(ticker)


if __name__ == "__main__":
    main()

import argparse
import logging
from orchestrator import FinancialAnalysisOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("Financial_Analysis_Runner")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run financial analysis for a company")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    args = parser.parse_args()
    
    ticker = args.ticker.upper()
    
    print(f"Running financial analysis for {ticker}...")
    
    try:
        orchestrator = FinancialAnalysisOrchestrator()
        results = orchestrator.analyze_company(ticker)
        
        if "error" in results:
            print(f"Analysis failed: {results['error']}")
        else:
            print(f"Analysis complete!")
            print(f"Report saved to: {results.get('report_path', 'unknown')}")
    
    except Exception as e:
        logger.error(f"Error running analysis: {str(e)}", exc_info=True)
        print(f"Error: {str(e)}")

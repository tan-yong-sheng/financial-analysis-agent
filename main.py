import os
import sys
import argparse
import logging
from datetime import datetime
from orchestrator import FinancialAnalysisOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("Financial_Analysis_Main")

def main():
    """Main function to run the financial analysis system."""
    parser = argparse.ArgumentParser(description="Financial Analysis System")
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker symbol to analyze")
    parser.add_argument("--output", type=str, default="reports", help="Output directory for reports")
    
    args = parser.parse_args()
    ticker = args.ticker.upper()
    
    logger.info(f"Starting analysis for {ticker}")
    
    try:
        orchestrator = FinancialAnalysisOrchestrator()
        result = orchestrator.analyze_company(ticker)
        
        if "error" in result:
            print(f"\nError analyzing {ticker}: {result['error']}\n")
        else:
            print("\n" + "="*50)
            print(f"Analysis for {ticker} completed successfully!")
            print(f"Full report saved to: {os.path.abspath(result['report_path'])}")
            print(f"Results summary saved to: {os.path.abspath(result['results_path'])}")
            print("="*50 + "\n")
            
    except Exception as e:
        logger.error(f"Error analyzing {ticker}: {str(e)}")
        print(f"\nError analyzing {ticker}: {str(e)}\n")

if __name__ == "__main__":
    main()

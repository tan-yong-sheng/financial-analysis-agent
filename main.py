import os
import argparse
import logging
from orchestrator import FinancialAnalysisOrchestrator
from config import REPORTS_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("financial_analysis.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Financial_Analysis_Main")

def main():
    """Main entry point for financial analysis tool."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate financial analysis report for a company")
    parser.add_argument("--ticker", type=str, required=True, help="Ticker symbol of the company to analyze")
    parser.add_argument("--output", type=str, default=None, help="Output directory for reports (default: ./reports)")
    
    args = parser.parse_args()
    ticker = args.ticker.upper()
    output_dir = args.output if args.output else REPORTS_DIR
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Initialize orchestrator
        logger.info(f"Starting analysis for {ticker}")
        orchestrator = FinancialAnalysisOrchestrator()
        
        # Run analysis
        results = orchestrator.analyze_company(ticker)
        
        # Check for successful completion
        if "error" not in results:
            report_path = results.get("report_path", "unknown")
            results_path = results.get("results_path", "unknown")
            
            print("\n" + "="*50)
            print(f"Analysis for {ticker} completed successfully!")
            print(f"Full report saved to: {report_path}")
            print(f"Results summary saved to: {results_path}")
            print("="*50 + "\n")
        else:
            print(f"\nError analyzing {ticker}: {results['error']}\n")
            
    except Exception as e:
        logger.error(f"Error analyzing {ticker}", exc_info=True)
        print(f"\nError analyzing {ticker}: {str(e)}\n")
        
if __name__ == "__main__":
    main()

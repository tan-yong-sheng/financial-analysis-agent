import os
import json
import time
from typing import Dict, Any, List
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.planner_agent import PlannerAgent
from agents.data_collection_agent import DataCollectionAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.writer_agent import WriterAgent
from agents.fact_check_agent import FactCheckAgent
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

logger = logging.getLogger("Financial_Analysis_Orchestrator")

class FinancialAnalysisOrchestrator:
    """Orchestrates the workflow between different specialized agents."""
    
    def __init__(self):
        logger.info("Initializing Financial Analysis Orchestrator")
        
        # Configure OpenAI settings from environment
        self.openai_base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        self.model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4')
        
        # Initialize agents with configuration
        self.planner = PlannerAgent(base_url=self.openai_base_url, model_name=self.model_name)
        self.data_collector = DataCollectionAgent(base_url=self.openai_base_url, model_name=self.model_name)
        self.researcher = ResearchAgent(base_url=self.openai_base_url, model_name=self.model_name)
        self.analyst = AnalysisAgent(base_url=self.openai_base_url, model_name=self.model_name)
        self.writer = WriterAgent(base_url=self.openai_base_url, model_name=self.model_name)
        self.fact_checker = FactCheckAgent(base_url=self.openai_base_url, model_name=self.model_name)
        
        # Create reports directory if it doesn't exist
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
    def analyze_company(self, ticker: str) -> Dict[str, Any]:
        """
        Execute the full financial analysis workflow for a company.
        
        Args:
            ticker (str): The ticker symbol of the company to analyze.
            
        Returns:
            dict: The final analysis results including the report.
        """
        results = {"ticker": ticker}
        start_time = time.time()
        
        try:
            logger.info(f"Starting analysis for {ticker}")
            
            # Step 1: Initial data gathering to get company profile
            logger.info("Getting initial company data for planning")
            initial_data = {
                "ticker": ticker
            }
            collected_data = self.data_collector.process(initial_data)
            results["company_profile"] = collected_data.get("company_profile", [])
            
            # Extract company info for planning
            company_info = {}
            if isinstance(results["company_profile"], list) and len(results["company_profile"]) > 0:
                company_info = results["company_profile"][0]
            
            # Step 2: Create research plan
            logger.info("Creating research plan")
            planning_input = {
                "ticker": ticker,
                "company_info": company_info
            }
            research_plan = self.planner.process(planning_input)
            results["research_plan"] = research_plan
            
            # Step 3: Collect detailed financial data based on the research plan
            logger.info("Collecting detailed financial data based on plan")
            data_collection_input = {
                "ticker": ticker,
                "research_plan": research_plan
            }
            financial_data = self.data_collector.process(data_collection_input)
            results["financial_data"] = financial_data
            
            # Step 4: Research market, industry, and competitors
            logger.info("Conducting market and industry research")
            research_input = {
                "ticker": ticker,
                "company_profile": results["company_profile"],
                "research_plan": research_plan
            }
            research_results = self.researcher.process(research_input)
            results["research_results"] = research_results
            
            # Step 5: Analyze financial data and integrate with research
            logger.info("Analyzing financial data and integrating with research")
            analysis_input = {
                "financial_data": financial_data,
                "research_results": research_results,
                "research_plan": research_plan
            }
            analysis_results = self.analyst.process(analysis_input)
            results["analysis_results"] = analysis_results
            
            # Step 6: Generate the research report
            logger.info("Writing financial research report")
            report_input = {
                "ticker": ticker,
                "company_profile": results["company_profile"],
                "research_plan": research_plan,
                "analysis_results": analysis_results
            }
            report_results = self.writer.process(report_input)
            results["report"] = report_results.get("report", "")  # Get the actual report content
            
            # Step 7: Fact check and improve the report
            logger.info("Fact checking and validating the report")
            fact_check_input = {
                "report": results["report"],
                "financial_data": financial_data,
                "analysis_results": analysis_results,
                "research_results": research_results
            }
            fact_check_results = self.fact_checker.process(fact_check_input)
            results["validation_results"] = fact_check_results.get("validation_results", {})
            
            # Save the improved report as Markdown
            final_report = fact_check_results.get("improved_report", results["report"])
            
            # Create report directory if it doesn't exist
            os.makedirs(REPORTS_DIR, exist_ok=True)
            
            # Save as Markdown file
            report_path = os.path.join(REPORTS_DIR, f"{ticker}_analysis.md")
            with open(report_path, "w", encoding='utf-8') as f:
                f.write(final_report)
            
            # Also save results as JSON (using custom encoder for numpy types)
            results_path = os.path.join(REPORTS_DIR, f"{ticker}_results.json")
            with open(results_path, "w", encoding='utf-8') as f:
                # Store paths in results
                results["report_path"] = report_path
                results["results_path"] = results_path
                json.dump(results, f, indent=2, default=str)
            
            execution_time = time.time() - start_time
            results["execution_time"] = execution_time
            logger.info(f"Analysis completed for {ticker} in {execution_time:.2f} seconds")
            logger.info(f"Report saved to {report_path}")
            logger.info(f"Results saved to {results_path}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during analysis for {ticker}: {str(e)}", exc_info=True)
            execution_time = time.time() - start_time
            return {
                "ticker": ticker,
                "error": str(e),
                "execution_time": execution_time,
                "partial_results": results
            }

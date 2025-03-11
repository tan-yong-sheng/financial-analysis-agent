import os
import time
import json
from typing import Dict, Any
import logging

from agents.analysis_agent import AnalysisAgent
from agents.research_agent import ResearchAgent
from agents.report_agent import ReportAgent
from agents.data_collection_agent import DataCollectionAgent
from utils.citation_validator import log_source_summary, check_citations_in_analysis

logger = logging.getLogger(__name__)

class FinancialAnalysisOrchestrator:
    """Orchestrates the financial analysis workflow."""
    
    def __init__(self):
        """Initialize the orchestrator with required agents."""
        self.data_collector = DataCollectionAgent()
        self.researcher = ResearchAgent()
        self.analyst = AnalysisAgent()
        self.report_generator = ReportAgent()

    def analyze_company(self, ticker: str) -> Dict[str, Any]:
        """Run complete analysis for a company."""
        start_time = time.time()
        
        try:
            # Initial company data
            company_data = self._get_initial_company_data(ticker)
            
            # Create research plan
            research_plan = self._create_research_plan({
                "ticker": ticker,
                "company_data": company_data
            })
            
            # Collect financial data
            financial_data = self._collect_financial_data({
                "ticker": ticker,
                "research_plan": research_plan
            })
            
            # Conduct market research
            research_results = self._conduct_market_research({
                "ticker": ticker,
                "company_data": company_data,
                "research_plan": research_plan
            })
            
            # Analyze data
            analysis_results = self._analyze_data_and_research({
                "financial_data": financial_data,
                "research_results": research_results,
                "research_plan": research_plan
            })
            
            # Write results to files
            self._write_output_files(ticker, analysis_results)
            
            execution_time = time.time() - start_time
            
            return {
                "ticker": ticker,
                "execution_time": execution_time,
                "report_path": f"reports/{ticker}_analysis.md",
                "results_path": f"reports/{ticker}_results.json"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {str(e)}")
            return {"error": str(e)}

    def _get_initial_company_data(self, ticker: str) -> Dict[str, Any]:
        """Get initial company data."""
        return self.data_collector.get_company_profile(ticker)

    def _create_research_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a research plan."""
        return self.researcher.create_research_plan(input_data)

    def _collect_financial_data(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect all required financial data."""
        return self.data_collector.process(input_data)

    def _conduct_market_research(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct market research."""
        return self.researcher.process(input_data)

    def _analyze_data_and_research(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze collected data."""
        # Ensure source citations are preserved
        financial_data = input_data.get("financial_data", {})
        research_results = input_data.get("research_results", {})
        
        # Log source information for debugging
        logger.info("Checking financial data sources:")
        log_source_summary(financial_data)
        
        logger.info("Checking research sources:")
        if "sources" in research_results:
            log_source_summary(research_results["sources"])
        
        # Create a record of all sources used
        sources = {
            "financial_data_sources": self._extract_sources(financial_data),
            "research_sources": research_results.get("sources", {})
        }
        
        # Add sources to input data
        input_data["sources"] = sources
        
        # Process with analysis agent
        analysis_results = self.analyst.process(input_data)
        
        # Ensure sources are preserved in the results
        if "sources" not in analysis_results:
            analysis_results["sources"] = sources
        
        # Check citations in analysis results
        citation_stats = check_citations_in_analysis(analysis_results)
        analysis_results["citation_stats"] = citation_stats
            
        return analysis_results

    def _extract_sources(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract source information from financial data."""
        sources = {}
        
        # Process common data types
        for key, value in data.items():
            if isinstance(value, dict) and "_source" in value:
                sources[key] = value["_source"]
            elif isinstance(value, list) and value and isinstance(value[0], dict) and "_source" in value[0]:
                sources[key] = value[0]["_source"]  # Use the first item's source info
                
        return sources

    def _write_output_files(self, ticker: str, analysis_results: Dict[str, Any]) -> None:
        """Write analysis results to files."""
        # Ensure reports directory exists
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir, exist_ok=True)
        
        # Generate report
        report_result = self.report_generator.process({
            "ticker": ticker,
            "analysis_results": analysis_results
        })
        
        # Write markdown report
        with open(f"{reports_dir}/{ticker}_analysis.md", 'w') as f:
            f.write(report_result["report"])
            
        # Write JSON results
        with open(f"{reports_dir}/{ticker}_results.json", 'w') as f:
            json.dump(analysis_results, f, indent=2)

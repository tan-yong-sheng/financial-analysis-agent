import sys
import os
import json
from typing import Dict, Any, List, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent
from modules.data_collector import FinancialDataCollector
from config import DEFAULT_PERIOD, DEFAULT_LIMIT, TECHNICAL_INDICATORS

class DataCollectionAgent(BaseAgent):
    """Agent responsible for collecting financial data."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a financial data collection specialist that gathers accurate financial information"
        super().__init__(role, "Data Collection", base_url=base_url, model_name=model_name)
        self.collector = FinancialDataCollector()
        
    def determine_data_needs(self, ticker: str, research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine what data needs to be collected based on the research plan.
        
        Args:
            ticker (str): The ticker symbol of the company.
            research_plan (dict): The research plan from the planner agent.
            
        Returns:
            dict: Data collection plan with specific endpoints and parameters.
        """
        # Get insights from LLM on what specific data is needed
        prompt = f"""
        Based on the following research plan for {ticker}, determine exactly what financial data needs to be collected.
        Research plan: {json.dumps(research_plan, indent=2)}
        
        Create a specific data collection plan that includes:
        1. Which financial statements are needed (income statement, balance sheet, cash flow) and for what periods
        2. Which technical indicators should be calculated
        3. Which company metrics and ratios should be collected
        4. Any other specific data points mentioned in the research plan
        
        Format your response as a JSON object with:
        - financial_statements: list of statements to collect
        - statement_period: quarterly or annual
        - statement_limit: how many periods to collect
        - technical_indicators: list of technical indicators to calculate
        - ratios_and_metrics: list of specific ratios and metrics to collect
        - competitor_tickers: list of competitor tickers to also collect data for (if mentioned)
        """
        
        try:
            response = self._call_llm(prompt)
            data_plan = json.loads(response)
            return data_plan
        except json.JSONDecodeError:
            # Default data collection plan if LLM response isn't valid JSON
            return {
                "financial_statements": ["income_statement", "balance_sheet", "cash_flow"],
                "statement_period": DEFAULT_PERIOD,
                "statement_limit": DEFAULT_LIMIT,
                "technical_indicators": TECHNICAL_INDICATORS,
                "ratios_and_metrics": ["key_metrics", "financial_ratios"],
                "competitor_tickers": []
            }
    
    def collect_company_data(self, ticker: str, data_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect data for a company based on the data collection plan.
        
        Args:
            ticker (str): The ticker symbol of the company.
            data_plan (dict): The data collection plan.
            
        Returns:
            dict: Collected financial data.
        """
        period = data_plan.get("statement_period", DEFAULT_PERIOD)
        limit = data_plan.get("statement_limit", DEFAULT_LIMIT)
        
        collected_data = {
            "ticker": ticker,
            "company_profile": self.collector.get_company_profile(ticker),
            "stock_price": self.collector.get_stock_price(ticker)
        }
        
        # Collect financial statements
        statements = data_plan.get("financial_statements", ["income_statement", "balance_sheet", "cash_flow"])
        if "income_statement" in statements:
            collected_data["income_statement"] = self.collector.get_income_statement(ticker, period, limit)
        if "balance_sheet" in statements:
            collected_data["balance_sheet"] = self.collector.get_balance_sheet(ticker, period, limit)
        if "cash_flow" in statements:
            collected_data["cash_flow"] = self.collector.get_cash_flow(ticker, period, limit)
            
        # Collect ratios and metrics
        ratios_metrics = data_plan.get("ratios_and_metrics", [])
        if "key_metrics" in ratios_metrics:
            collected_data["key_metrics"] = self.collector.get_key_metrics(ticker, period, limit)
        if "financial_ratios" in ratios_metrics:
            collected_data["financial_ratios"] = self.collector.get_financial_ratios(ticker, period, limit)
        if "analyst_estimates" in ratios_metrics:
            collected_data["analyst_estimates"] = self.collector.get_analyst_estimates(ticker)
            
        # Collect technical indicators
        technical_indicators = data_plan.get("technical_indicators", TECHNICAL_INDICATORS)
        indicators_data = {}
        for indicator in technical_indicators:
            time_period = 14  # Default time period
            if isinstance(indicator, dict):
                indicator_name = indicator.get("name")
                time_period = indicator.get("time_period", 14)
            else:
                indicator_name = indicator
                
            indicators_data[indicator_name] = self.collector.get_technical_indicators(
                ticker, indicator_name, time_period
            )
            
        collected_data["technical_indicators"] = indicators_data
        
        # Collect competitor data if specified
        competitor_tickers = data_plan.get("competitor_tickers", [])
        if competitor_tickers:
            competitors_data = {}
            for comp_ticker in competitor_tickers:
                # Collect basic info for competitors
                competitors_data[comp_ticker] = {
                    "company_profile": self.collector.get_company_profile(comp_ticker),
                    "key_metrics": self.collector.get_key_metrics(comp_ticker, period, limit)
                }
            collected_data["competitors"] = competitors_data
            
        return collected_data
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data to collect financial information.
        
        Args:
            input_data (dict): Input data containing ticker and research plan.
            
        Returns:
            dict: Collected financial data.
        """
        ticker = input_data.get("ticker")
        research_plan = input_data.get("research_plan", {})
        
        if not ticker:
            return {"error": "No ticker symbol provided"}
        
        data_plan = self.determine_data_needs(ticker, research_plan)
        return self.collect_company_data(ticker, data_plan)

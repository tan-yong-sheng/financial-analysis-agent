import sys
import os
import json
import requests
from typing import Dict, Any, List, Optional
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent
from config import FMP_API_KEY, FMP_BASE_URL, DEFAULT_PERIOD, DEFAULT_LIMIT, TECHNICAL_INDICATORS
from tools.data_transformer import clean_and_convert_numeric, convert_numpy_types

logger = logging.getLogger(__name__)

class DataCollectionAgent(BaseAgent):
    """Agent responsible for collecting financial data from various sources."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        """Initialize data collection agent."""
        role = "a data collection specialist that gathers financial data from various sources"
        super().__init__(role, "Data Collector", base_url=base_url, model_name=model_name)
        self.api_key = FMP_API_KEY
        self.base_url = FMP_BASE_URL
    
    def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        """
        Get company profile information.
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            dict: Company profile data with source information
        """
        try:
            url = f"{self.base_url}/profile/{ticker}?apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            profile_data = response.json()
            
            if not profile_data or not isinstance(profile_data, list) or len(profile_data) == 0:
                logger.warning(f"No profile data found for {ticker}")
                return {"error": f"No company profile found for {ticker}"}
            
            # Add source information to the data    
            result = profile_data[0]  # FMP returns a list with one item
            result["_source"] = {
                "name": "Financial Modeling Prep API",
                "endpoint": f"profile/{ticker}",
                "date_retrieved": self._get_current_date(),
                "url": url.split('?')[0]  # Remove API key from URL
            }
                
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching company profile for {ticker}: {str(e)}")
            return {"error": f"Failed to fetch company profile: {str(e)}"}
    
    def _get_current_date(self) -> str:
        """Get current date as a string in ISO format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_income_statement(self, ticker: str, period: str = DEFAULT_PERIOD, limit: int = DEFAULT_LIMIT) -> List[Dict[str, Any]]:
        """Get income statement data."""
        try:
            url = f"{self.base_url}/income-statement/{ticker}?period={period}&limit={limit}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Add source information to each item
            source_info = {
                "name": "Financial Modeling Prep API",
                "endpoint": f"income-statement/{ticker}",
                "period": period,
                "date_retrieved": self._get_current_date(),
                "url": url.split('?')[0]  # Remove API key from URL
            }
            
            for item in data:
                item["_source"] = source_info
                
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching income statement for {ticker}: {str(e)}")
            return [{"error": f"Failed to fetch income statement: {str(e)}"}]
    
    def get_balance_sheet(self, ticker: str, period: str = DEFAULT_PERIOD, limit: int = DEFAULT_LIMIT) -> List[Dict[str, Any]]:
        """Get balance sheet data."""
        try:
            url = f"{self.base_url}/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Add source information to each item
            source_info = {
                "name": "Financial Modeling Prep API",
                "endpoint": f"balance-sheet-statement/{ticker}",
                "period": period,
                "date_retrieved": self._get_current_date(),
                "url": url.split('?')[0]  # Remove API key from URL
            }
            
            for item in data:
                item["_source"] = source_info
                
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching balance sheet for {ticker}: {str(e)}")
            return [{"error": f"Failed to fetch balance sheet: {str(e)}"}]
    
    def get_cash_flow(self, ticker: str, period: str = DEFAULT_PERIOD, limit: int = DEFAULT_LIMIT) -> List[Dict[str, Any]]:
        """Get cash flow statement data."""
        try:
            url = f"{self.base_url}/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Add source information to each item
            source_info = {
                "name": "Financial Modeling Prep API",
                "endpoint": f"cash-flow-statement/{ticker}",
                "period": period,
                "date_retrieved": self._get_current_date(),
                "url": url.split('?')[0]  # Remove API key from URL
            }
            
            for item in data:
                item["_source"] = source_info
                
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching cash flow statement for {ticker}: {str(e)}")
            return [{"error": f"Failed to fetch cash flow statement: {str(e)}"}]
    
    def get_technical_indicators(self, ticker: str, indicator_name: str = None, time_period: int = 14) -> Dict[str, Any]:
        """
        Get technical indicators data.
        
        Args:
            ticker (str): The ticker symbol
            indicator_name (str, optional): Specific indicator to fetch
            time_period (int, optional): Time period for the indicator
            
        Returns:
            dict: Technical indicators data with source information
        """
        indicators = {}
        
        # If a specific indicator is requested
        if indicator_name:
            try:
                url = f"{self.base_url}/technical_indicator/daily/{ticker}?type={indicator_name}&period={time_period}&apikey={self.api_key}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                # Add source information
                source_info = {
                    "name": "Financial Modeling Prep API",
                    "endpoint": f"technical_indicator/daily/{ticker}",
                    "indicator": indicator_name,
                    "period": time_period,
                    "date_retrieved": self._get_current_date(),
                    "url": url.split('?')[0]  # Remove API key from URL
                }
                
                return {
                    "historical": data,
                    "_source": source_info
                }
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching {indicator_name} for {ticker}: {str(e)}")
                return {"error": f"Failed to fetch {indicator_name}: {str(e)}"}
        
        # If no specific indicator, fetch all from config
        for indicator in TECHNICAL_INDICATORS:
            try:
                url = f"{self.base_url}/technical_indicator/daily/{ticker}?type={indicator}&period={time_period}&apikey={self.api_key}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                # Add source information
                source_info = {
                    "name": "Financial Modeling Prep API",
                    "endpoint": f"technical_indicator/daily/{ticker}",
                    "indicator": indicator,
                    "period": time_period,
                    "date_retrieved": self._get_current_date(),
                    "url": url.split('?')[0]  # Remove API key from URL
                }
                
                indicators[indicator] = {
                    "historical": data,
                    "_source": source_info
                }
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching {indicator} for {ticker}: {str(e)}")
                indicators[indicator] = {"error": f"Failed to fetch {indicator}: {str(e)}"}
        
        return indicators
    
    def collect_financial_data(self, ticker: str) -> Dict[str, Any]:
        """Collect comprehensive financial data for a company."""
        company_profile = self.get_company_profile(ticker)
        income_statement = self.get_income_statement(ticker)
        balance_sheet = self.get_balance_sheet(ticker)
        cash_flow = self.get_cash_flow(ticker)
        technical_indicators = self.get_technical_indicators(ticker)
        
        return {
            "company_profile": company_profile,
            "income_statement": income_statement,
            "balance_sheet": balance_sheet,
            "cash_flow": cash_flow,
            "technical_indicators": technical_indicators
        }
    
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
        """Collect data for a company based on the data collection plan."""
        period = data_plan.get("statement_period", DEFAULT_PERIOD)
        limit = data_plan.get("statement_limit", DEFAULT_LIMIT)
        
        collected_data = {
            "ticker": ticker,
            "company_profile": self.get_company_profile(ticker),
            "stock_price": self.get_stock_price(ticker) if hasattr(self, 'get_stock_price') else None
        }
        
        # Collect financial statements
        statements = data_plan.get("financial_statements", ["income_statement", "balance_sheet", "cash_flow"])
        if "income_statement" in statements:
            collected_data["income_statement"] = self.get_income_statement(ticker, period, limit)
        if "balance_sheet" in statements:
            collected_data["balance_sheet"] = self.get_balance_sheet(ticker, period, limit)
        if "cash_flow" in statements:
            collected_data["cash_flow"] = self.get_cash_flow(ticker, period, limit)
            
        # Collect ratios and metrics
        ratios_metrics = data_plan.get("ratios_and_metrics", [])
        if "key_metrics" in ratios_metrics:
            collected_data["key_metrics"] = self.get_key_metrics(ticker, period, limit) if hasattr(self, 'get_key_metrics') else None
        if "financial_ratios" in ratios_metrics:
            collected_data["financial_ratios"] = self.get_financial_ratios(ticker, period, limit) if hasattr(self, 'get_financial_ratios') else None
        if "analyst_estimates" in ratios_metrics:
            collected_data["analyst_estimates"] = self.get_analyst_estimates(ticker) if hasattr(self, 'get_analyst_estimates') else None
            
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
                
            if hasattr(self, 'get_technical_indicators'):
                indicators_data[indicator_name] = self.get_technical_indicators(
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
                    "company_profile": self.get_company_profile(comp_ticker),
                    "key_metrics": self.get_key_metrics(comp_ticker, period, limit) if hasattr(self, 'get_key_metrics') else None
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
    
    def get_stock_price(self, ticker: str) -> Dict[str, Any]:
        """Get historical stock price data."""
        try:
            url = f"{self.base_url}/historical-price-full/{ticker}?apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Add source information
            data["_source"] = {
                "name": "Financial Modeling Prep API",
                "endpoint": f"historical-price-full/{ticker}",
                "date_retrieved": self._get_current_date(),
                "url": url.split('?')[0]  # Remove API key from URL
            }
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching stock price data for {ticker}: {str(e)}")
            return {"error": f"Failed to fetch stock price data: {str(e)}"}

    def get_key_metrics(self, ticker: str, period: str = DEFAULT_PERIOD, limit: int = DEFAULT_LIMIT) -> List[Dict[str, Any]]:
        """Get key company metrics."""
        try:
            url = f"{self.base_url}/key-metrics/{ticker}?period={period}&limit={limit}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Add source information to each item
            source_info = {
                "name": "Financial Modeling Prep API",
                "endpoint": f"key-metrics/{ticker}",
                "period": period,
                "date_retrieved": self._get_current_date(),
                "url": url.split('?')[0]  # Remove API key from URL
            }
            
            for item in data:
                item["_source"] = source_info
                
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching key metrics for {ticker}: {str(e)}")
            return [{"error": f"Failed to fetch key metrics: {str(e)}"}]

    def get_financial_ratios(self, ticker: str, period: str = DEFAULT_PERIOD, limit: int = DEFAULT_LIMIT) -> List[Dict[str, Any]]:
        """Get financial ratios."""
        try:
            url = f"{self.base_url}/ratios/{ticker}?period={period}&limit={limit}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Add source information to each item
            source_info = {
                "name": "Financial Modeling Prep API",
                "endpoint": f"ratios/{ticker}",
                "period": period,
                "date_retrieved": self._get_current_date(),
                "url": url.split('?')[0]  # Remove API key from URL
            }
            
            for item in data:
                item["_source"] = source_info
                
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching financial ratios for {ticker}: {str(e)}")
            return [{"error": f"Failed to fetch financial ratios: {str(e)}"}]

    def get_analyst_estimates(self, ticker: str) -> List[Dict[str, Any]]:
        """Get analyst estimates."""
        try:
            url = f"{self.base_url}/analyst-estimates/{ticker}?apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Add source information to each item
            source_info = {
                "name": "Financial Modeling Prep API",
                "endpoint": f"analyst-estimates/{ticker}",
                "date_retrieved": self._get_current_date(),
                "url": url.split('?')[0]  # Remove API key from URL
            }
            
            for item in data:
                item["_source"] = source_info
                
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching analyst estimates for {ticker}: {str(e)}")
            return [{"error": f"Failed to fetch analyst estimates: {str(e)}"}]

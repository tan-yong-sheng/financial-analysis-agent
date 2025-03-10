import os
import requests
import json
from typing import Dict, Any, List, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import FMP_API_KEY, FMP_BASE_URL

logger = logging.getLogger("Financial_Data_Provider")

class FinancialDataProvider:
    """Provider for financial data from the Financial Modeling Prep API."""
    
    def __init__(self):
        """Initialize the financial data provider with API key."""
        self.api_key = FMP_API_KEY
        if not self.api_key:
            logger.warning("FMP_API_KEY not found in environment variables")
        self.base_url = FMP_BASE_URL
        
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to the FMP API.
        
        Args:
            endpoint (str): API endpoint to call
            params (dict, optional): Query parameters
            
        Returns:
            dict: Response data
        """
        if params is None:
            params = {}
        
        # Add API key to parameters
        params['apikey'] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error when calling {url}: {str(e)}")
            return {"error": str(e)}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error when calling {url}: {str(e)}")
            return {"error": str(e)}
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON response from {url}")
            return {"error": "Invalid JSON response"}

    def get_company_profile(self, ticker: str) -> List[Dict[str, Any]]:
        """
        Get company profile information.
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            list: Company profile data
        """
        return self._make_request(f"profile/{ticker}")
    
    def get_income_statement(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get income statement data.
        
        Args:
            ticker (str): Company ticker symbol
            period (str): 'annual' or 'quarter'
            limit (int): Number of periods to retrieve
            
        Returns:
            list: Income statement data
        """
        return self._make_request(f"income-statement/{ticker}", {
            "period": period,
            "limit": limit
        })
    
    def get_balance_sheet(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get balance sheet data.
        
        Args:
            ticker (str): Company ticker symbol
            period (str): 'annual' or 'quarter'
            limit (int): Number of periods to retrieve
            
        Returns:
            list: Balance sheet data
        """
        return self._make_request(f"balance-sheet-statement/{ticker}", {
            "period": period,
            "limit": limit
        })
    
    def get_cash_flow(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get cash flow statement data.
        
        Args:
            ticker (str): Company ticker symbol
            period (str): 'annual' or 'quarter'
            limit (int): Number of periods to retrieve
            
        Returns:
            list: Cash flow statement data
        """
        return self._make_request(f"cash-flow-statement/{ticker}", {
            "period": period,
            "limit": limit
        })
    
    def get_key_metrics(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get key company metrics.
        
        Args:
            ticker (str): Company ticker symbol
            period (str): 'annual' or 'quarter'
            limit (int): Number of periods to retrieve
            
        Returns:
            list: Key metrics data
        """
        return self._make_request(f"key-metrics/{ticker}", {
            "period": period,
            "limit": limit
        })
    
    def get_financial_ratios(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get financial ratios.
        
        Args:
            ticker (str): Company ticker symbol
            period (str): 'annual' or 'quarter'
            limit (int): Number of periods to retrieve
            
        Returns:
            list: Financial ratios data
        """
        return self._make_request(f"ratios/{ticker}", {
            "period": period,
            "limit": limit
        })
    
    def get_stock_price(self, ticker: str, timeseries: int = 365) -> Dict[str, Any]:
        """
        Get historical stock price data.
        
        Args:
            ticker (str): Company ticker symbol
            timeseries (int): Number of days of historical data
            
        Returns:
            dict: Historical stock price data
        """
        # Get historical daily prices
        historical_data = self._make_request(f"historical-price-full/{ticker}", {
            "timeseries": timeseries
        })
        
        # Get current quote
        quote_data = self._make_request(f"quote/{ticker}")
        
        return {
            "historical": historical_data.get("historical", []),
            "current_quote": quote_data[0] if isinstance(quote_data, list) and len(quote_data) > 0 else {}
        }
    
    def get_analyst_estimates(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get analyst estimates.
        
        Args:
            ticker (str): Company ticker symbol
            period (str): 'annual' or 'quarter'
            limit (int): Number of periods to retrieve
            
        Returns:
            list: Analyst estimates data
        """
        return self._make_request(f"analyst-estimates/{ticker}", {
            "period": period,
            "limit": limit
        })
        
    def get_technical_indicators(self, ticker: str, indicator: str, time_period: int = 14) -> Dict[str, Any]:
        """
        Get technical indicators for a stock.
        
        Args:
            ticker (str): Company ticker symbol
            indicator (str): Technical indicator type (e.g., 'rsi', 'sma', 'ema')
            time_period (int): Time period for indicator calculation
            
        Returns:
            dict: Technical indicator data
        """
        # Technical indicators endpoint requires different URL structure
        indicator = indicator.lower()
        
        # Map indicator names to endpoints
        indicator_endpoints = {
            "sma": "technical_indicator/daily/sma",
            "ema": "technical_indicator/daily/ema",
            "wma": "technical_indicator/daily/wma",
            "rsi": "technical_indicator/daily/rsi",
            "macd": "technical_indicator/daily/macd"
        }
        
        # Use proper endpoint if available, default to RSI if not found
        endpoint = indicator_endpoints.get(indicator, "technical_indicator/daily/rsi")
        
        return self._make_request(f"{endpoint}/{ticker}", {
            "period": time_period
        })

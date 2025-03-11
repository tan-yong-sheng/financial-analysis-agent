import os
import requests
import json
from typing import Dict, Any, List, Optional
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import FMP_API_KEY, FMP_BASE_URL
from utils.observability import StructuredLogger, monitor_agent_method


class FinancialDataProvider:
    """Provider for financial data from the Financial Modeling Prep API."""
    
    def __init__(self):
        """Initialize the financial data provider with enhanced logging."""
        self.logger = StructuredLogger("financial_data_provider")
        self.api_key = FMP_API_KEY
        self.base_url = FMP_BASE_URL
        
        # Initialize request metrics
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
        
        if not self.api_key:
            self.logger.error("FMP_API_KEY not found in environment variables")
        
    @monitor_agent_method()
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
        start_time = time.time()
        
        # Track request timing
        if self.last_request_time:
            time_since_last_request = start_time - self.last_request_time
            if time_since_last_request < 1:  # Less than 1 second between requests
                self.logger.warning("High request frequency detected",
                                  time_between_requests=time_since_last_request)
        
        self.last_request_time = start_time
        self.request_count += 1
        
        # Log request attempt
        self.logger.debug("Making API request",
                         url=url,
                         endpoint=endpoint,
                         params={k: v for k, v in params.items() if k != 'apikey'})  # Don't log API key
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            execution_time = time.time() - start_time
            response_size = len(response.content)
            status_code = response.status_code
            
            # Log successful response
            self.logger.info("API request successful",
                           endpoint=endpoint,
                           status_code=status_code,
                           execution_time=execution_time,
                           response_size=response_size,
                           total_requests=self.request_count)
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            self.error_count += 1
            execution_time = time.time() - start_time
            
            # Check for rate limiting
            if e.response.status_code == 429:
                self.logger.error("Rate limit exceeded",
                                endpoint=endpoint,
                                execution_time=execution_time,
                                error_count=self.error_count,
                                headers=dict(e.response.headers))
            else:
                self.logger.error("HTTP error in API request",
                                endpoint=endpoint,
                                status_code=e.response.status_code,
                                execution_time=execution_time,
                                error_count=self.error_count,
                                error_message=str(e))
            return {"error": str(e)}
            
        except requests.exceptions.RequestException as e:
            self.error_count += 1
            execution_time = time.time() - start_time
            self.logger.error("Request error in API call",
                            endpoint=endpoint,
                            execution_time=execution_time,
                            error_count=self.error_count,
                            error_type=type(e).__name__,
                            error_message=str(e))
            return {"error": str(e)}
            
        except json.JSONDecodeError as e:
            self.error_count += 1
            execution_time = time.time() - start_time
            self.logger.error("Failed to decode JSON response",
                            endpoint=endpoint,
                            execution_time=execution_time,
                            error_count=self.error_count,
                            error_type=type(e).__name__,
                            error_message=str(e))
            return {"error": "Invalid JSON response"}

    @monitor_agent_method()
    def get_company_profile(self, ticker: str) -> List[Dict[str, Any]]:
        """
        Get company profile information.
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            list: Company profile data
        """
        return self._make_request(f"profile/{ticker}")
    
    @monitor_agent_method()
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
    
    @monitor_agent_method()
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
    
    @monitor_agent_method()
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
    
    @monitor_agent_method()
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
    
    @monitor_agent_method()
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
    
    @monitor_agent_method()
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
    
    @monitor_agent_method()
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
        
    @monitor_agent_method()
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

    @monitor_agent_method()
    def get_technical_indicator(self, ticker: str, indicator: str, time_period: int = 14) -> List[Dict[str, Any]]:
        """
        Get technical indicator data from Financial Modeling Prep API.
        
        Args:
            ticker (str): Company ticker symbol
            indicator (str): Indicator type ('rsi', 'macd', 'sma', 'ema')
            time_period (int): Time period for indicator calculation
            
        Returns:
            list: Technical indicator data
        """
        indicator = indicator.lower()
        
        # Map indicator names to their proper types
        indicator_types = {
            "sma": "sma",
            "ema": "ema",
            "wma": "wma",
            "rsi": "rsi",
            "macd": "macd"
        }
        
        if indicator not in indicator_types:
            self.logger.warning("Unsupported technical indicator",
                              ticker=ticker,
                              indicator=indicator,
                              supported_types=list(indicator_types.keys()))
            return []
            
        try:
            # All technical indicators use the same endpoint structure
            endpoint = "technical-indicator/daily"
            params = {
                "symbol": ticker,
                "type": indicator_types[indicator],
            }
            
            # Add period parameter for indicators that need it
            if indicator in ["sma", "ema", "wma", "rsi"]:
                params["period"] = time_period
                
            response = self._make_request(f"{endpoint}/{ticker}", params)
            
            # Check for valid response
            if isinstance(response, dict):
                if "error" in response:
                    self.logger.error("API error in technical indicator request",
                                    ticker=ticker,
                                    indicator=indicator,
                                    error_message=response['error'])
                    return []
                    
                data = response.get("technicalIndicator", [])
                self.logger.info("Technical indicator data retrieved",
                               ticker=ticker,
                               indicator=indicator,
                               data_points=len(data))
                return data
            elif isinstance(response, list):
                self.logger.info("Technical indicator data retrieved",
                               ticker=ticker,
                               indicator=indicator,
                               data_points=len(response))
                return response
            else:
                self.logger.warning("Unexpected technical indicator response format",
                                  ticker=ticker,
                                  indicator=indicator,
                                  response_type=type(response).__name__)
                return []
                
        except Exception as e:
            self.logger.error("Error fetching technical indicator",
                            ticker=ticker,
                            indicator=indicator,
                            error_type=type(e).__name__,
                            error_message=str(e))
            return []

    @monitor_agent_method()
    def check_api_status(self) -> Dict[str, Any]:
        """
        Check the status of the API key to identify quota issues.
        
        Returns:
            dict: API status information
        """
        try:
            endpoint = "status"
            response = self._make_request(endpoint)
            # Log API status metrics
            self.logger.info("API status check completed",
                           requests_made=self.request_count,
                           errors_encountered=self.error_count,
                           status=response)
            return response
        except Exception as e:
            self.logger.error("API status check failed",
                            error_type=type(e).__name__,
                            error_message=str(e),
                            requests_made=self.request_count,
                            errors_encountered=self.error_count)
            return {"error": str(e)}

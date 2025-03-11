import os
import sys
import json
from typing import Dict, Any, List, Optional
import time
from functools import wraps

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_data_provider import FinancialDataProvider
from utils.observability import StructuredLogger, monitor_agent_method


def validate_data(method):
    """Decorator to validate financial data responses."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = method(self, *args, **kwargs)
        
        # Get method parameters for logging
        params = {
            'ticker': args[0] if args else kwargs.get('ticker'),
            'period': kwargs.get('period', 'annual'),
            'limit': kwargs.get('limit', 5)
        }
        
        # Log validation results
        if isinstance(result, list):
            self.logger.info(f"{method.__name__} validation",
                           data_points=len(result),
                           execution_time=time.time() - start_time,
                           **params)
            
            if not result:
                self.logger.warning(f"No data returned from {method.__name__}",
                                  **params)
        
        elif isinstance(result, dict):
            self.logger.info(f"{method.__name__} validation",
                           fields=list(result.keys()),
                           execution_time=time.time() - start_time,
                           **params)
            
            # Check for empty or None values in dictionary
            empty_fields = [k for k, v in result.items() if not v]
            if empty_fields:
                self.logger.warning(f"Empty fields in {method.__name__}",
                                  empty_fields=empty_fields,
                                  **params)
        
        return result
    return wrapper

class FinancialDataCollector:
    """Module for collecting and organizing financial data."""
    
    def __init__(self):
        """Initialize the financial data collector with enhanced logging."""
        self.logger = StructuredLogger("financial_data_collector")
        self.provider = FinancialDataProvider()
        self.logger.info("Financial data collector initialized")
        
    @validate_data
    @monitor_agent_method()
    def get_company_profile(self, ticker: str) -> List[Dict[str, Any]]:
        """
        Get company profile information.
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            list: Company profile data
        """
        return self.provider.get_company_profile(ticker)
    
    @validate_data
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
        return self.provider.get_income_statement(ticker, period, limit)
    
    @validate_data
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
        return self.provider.get_balance_sheet(ticker, period, limit)
    
    @validate_data
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
        return self.provider.get_cash_flow(ticker, period, limit)
    
    @validate_data
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
        return self.provider.get_key_metrics(ticker, period, limit)
    
    @validate_data
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
        return self.provider.get_financial_ratios(ticker, period, limit)
    
    @validate_data
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
        return self.provider.get_stock_price(ticker, timeseries)
    
    @validate_data
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
        return self.provider.get_analyst_estimates(ticker, period, limit)
    
    @monitor_agent_method()
    def get_technical_indicators(self, ticker: str, indicator: str = None, time_period: int = 14) -> Dict[str, Any]:
        """
        Get technical indicators for a stock with enhanced logging and validation.
        
        Args:
            ticker (str): Company ticker symbol
            indicator (str, optional): Specific technical indicator type (e.g., 'rsi', 'sma', 'ema')
            time_period (int): Time period for indicator calculation
            
        Returns:
            dict: Technical indicator data
        """
        start_time = time.time()
        indicators = {'rsi': [], 'macd': [], 'sma': [], 'ema': []}
    
        try:
            self.logger.info("Starting technical indicators collection",
                           ticker=ticker,
                           indicator=indicator,
                           time_period=time_period)
            
            # Fetch each indicator type from the provider
            for ind_type in indicators.keys():
                try:
                    # Log the attempt to fetch indicator data
                    self.logger.debug(f"Fetching {ind_type.upper()} data",
                                    ticker=ticker,
                                    indicator_type=ind_type)
                    
                    # Only fetch the specified indicator if provided
                    if indicator and ind_type != indicator.lower():
                        continue
                    
                    # Call the provider to get the indicator data
                    start_indicator_time = time.time()
                    indicator_data = self.provider.get_technical_indicator(
                        ticker=ticker, 
                        indicator=ind_type, 
                        time_period=time_period
                    )
                    
                    # Store the result
                    if indicator_data:
                        indicators[ind_type] = indicator_data
                        self.logger.info("Indicator data fetched successfully",
                                       ticker=ticker,
                                       indicator_type=ind_type,
                                       data_points=len(indicator_data),
                                       execution_time=time.time() - start_indicator_time)
                    else:
                        self.logger.warning("No indicator data returned",
                                          ticker=ticker,
                                          indicator_type=ind_type)
                except Exception as e:
                    self.logger.error("Error fetching indicator",
                                    ticker=ticker,
                                    indicator_type=ind_type,
                                    error_type=type(e).__name__,
                                    error_message=str(e),
                                    execution_time=time.time() - start_indicator_time)
            
            # Validate results
            total_indicators = sum(1 for data in indicators.values() if data)
            self.logger.info("Technical indicators collection completed",
                           ticker=ticker,
                           total_indicators=total_indicators,
                           missing_indicators=len(indicators) - total_indicators,
                           execution_time=time.time() - start_time)
                    
            return indicators
        except Exception as e:
            self.logger.error("Technical indicators collection failed",
                            ticker=ticker,
                            error_type=type(e).__name__,
                            error_message=str(e),
                            execution_time=time.time() - start_time)
            # Return empty but structured data for graceful degradation
            return indicators
    
    @monitor_agent_method()
    def get_comprehensive_data(self, ticker: str, period: str = "annual", limit: int = 5) -> Dict[str, Any]:
        """
        Get comprehensive financial data for a company.
        
        Args:
            ticker (str): Company ticker symbol
            period (str): 'annual' or 'quarter'
            limit (int): Number of periods to retrieve
            
        Returns:
            dict: Comprehensive financial data
        """
        start_time = time.time()
        self.logger.info("Starting comprehensive data collection",
                        ticker=ticker,
                        period=period,
                        limit=limit)
        
        result = {
            "company_profile": self.get_company_profile(ticker),
            "income_statement": self.get_income_statement(ticker, period, limit),
            "balance_sheet": self.get_balance_sheet(ticker, period, limit),
            "cash_flow": self.get_cash_flow(ticker, period, limit),
            "key_metrics": self.get_key_metrics(ticker, period, limit),
            "financial_ratios": self.get_financial_ratios(ticker, period, limit),
            "stock_price": self.get_stock_price(ticker),
            "analyst_estimates": self.get_analyst_estimates(ticker, period, limit)
        }
        
        # Validate comprehensive data
        missing_data = [k for k, v in result.items() if not v]
        if missing_data:
            self.logger.warning("Missing data in comprehensive collection",
                              ticker=ticker,
                              missing_sections=missing_data)
        
        self.logger.info("Comprehensive data collection completed",
                        ticker=ticker,
                        sections=len(result),
                        complete_sections=len(result) - len(missing_data),
                        execution_time=time.time() - start_time)
        
        return result

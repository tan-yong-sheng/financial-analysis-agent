import os
import sys
import json
from typing import Dict, Any, List, Optional
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_data_provider import FinancialDataProvider

logger = logging.getLogger("Financial_Data_Collector")

class FinancialDataCollector:
    """Module for collecting and organizing financial data."""
    
    def __init__(self):
        """Initialize the financial data collector."""
        self.provider = FinancialDataProvider()
        
    def get_company_profile(self, ticker: str) -> List[Dict[str, Any]]:
        """
        Get company profile information.
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            list: Company profile data
        """
        return self.provider.get_company_profile(ticker)
    
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
    
    def get_technical_indicators(self, ticker: str, indicator: str = None, time_period: int = 14) -> Dict[str, Any]:
        """
        Get technical indicators for a stock.
        
        Args:
            ticker (str): Company ticker symbol
            indicator (str, optional): Specific technical indicator type (e.g., 'rsi', 'sma', 'ema')
            time_period (int): Time period for indicator calculation
            
        Returns:
            dict: Technical indicator data
        """
        indicators = {'rsi': [], 'sma': [], 'ema': []}
    
        try:
            # Fetch each indicator type from the provider
            for ind_type in indicators.keys():
                try:
                    # Log the attempt to fetch indicator data
                    logger.debug(f"Fetching {ind_type.upper()} data for {ticker}")
                    
                    # Only fetch the specified indicator if provided
                    if indicator and ind_type != indicator.lower():
                        continue
                    
                    # Call the provider to get the indicator data
                    indicator_data = self.provider.get_technical_indicator(
                        ticker=ticker, 
                        indicator=ind_type, 
                        time_period=time_period
                    )
                    
                    # Store the result
                    if indicator_data:
                        indicators[ind_type] = indicator_data
                        logger.info(f"Successfully fetched {len(indicator_data)} {ind_type.upper()} data points for {ticker}")
                    else:
                        logger.warning(f"No {ind_type.upper()} data returned for {ticker}")
                except Exception as e:
                    # Log indicator-specific errors but continue with other indicators
                    logger.error(f"Error fetching {ind_type} for {ticker}: {str(e)}")
            
            # Log validation for each indicator type
            for indicator_name, data in indicators.items():
                if not data:
                    logger.warning(f"No {indicator_name.upper()} data found for {ticker}. This may affect analysis quality.")
                    
            return indicators
        except Exception as e:
            logger.error(f"Error fetching technical indicators for {ticker}: {str(e)}")
            # Return empty but structured data for graceful degradation
            return indicators
    
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
        return {
            "company_profile": self.get_company_profile(ticker),
            "income_statement": self.get_income_statement(ticker, period, limit),
            "balance_sheet": self.get_balance_sheet(ticker, period, limit),
            "cash_flow": self.get_cash_flow(ticker, period, limit),
            "key_metrics": self.get_key_metrics(ticker, period, limit),
            "financial_ratios": self.get_financial_ratios(ticker, period, limit),
            "stock_price": self.get_stock_price(ticker),
            "analyst_estimates": self.get_analyst_estimates(ticker, period, limit)
        }

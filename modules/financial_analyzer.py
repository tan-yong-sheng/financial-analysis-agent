import sys
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.data_transformer import clean_and_convert_numeric, convert_numpy_types

logger = logging.getLogger("Financial_Analyzer")

class FinancialAnalyzer:
    """
    Module for analyzing financial data from various statements and indicators.
    
    This class provides methods to analyze income statements, balance sheets,
    cash flow statements, and technical indicators to extract insights and
    calculate important financial metrics.
    """
    
    def __init__(self):
        """Initialize the financial analyzer."""
        pass
        
    def analyze_income_statement(self, income_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze income statement data to extract revenue trends, profitability metrics, and growth rates.
        
        This method calculates key income statement metrics including:
        - Revenue growth rates
        - Net income growth rates
        - Gross, operating, and profit margins
        
        Args:
            income_data (list): Income statement data as a list of dictionaries
            
        Returns:
            dict: Income statement analysis results with summary, growth metrics, and margin calculations
        """
        try:
            # Convert to DataFrame for easier analysis
            if not income_data or not isinstance(income_data, list):
                return {"error": "Invalid income statement data"}
                
            df = pd.DataFrame(income_data)
            df = clean_and_convert_numeric(df)
            
            # Calculate growth rates
            if 'revenue' in df.columns:
                # Calculate YoY revenue growth (negative index because data is typically in reverse chronological order)
                df['revenue_growth'] = df['revenue'].pct_change(-1) * 100
                
            if 'netIncome' in df.columns:
                # Calculate YoY net income growth
                df['net_income_growth'] = df['netIncome'].pct_change(-1) * 100
                
            # Calculate profit margins
            if 'grossProfit' in df.columns and 'revenue' in df.columns:
                # Gross margin = Gross profit / Revenue
                df['gross_margin'] = (df['grossProfit'] / df['revenue']) * 100
                
            if 'operatingIncome' in df.columns and 'revenue' in df.columns:
                # Operating margin = Operating income / Revenue
                df['operating_margin'] = (df['operatingIncome'] / df['revenue']) * 100
                
            if 'netIncome' in df.columns and 'revenue' in df.columns:
                # Net profit margin = Net income / Revenue
                df['profit_margin'] = (df['netIncome'] / df['revenue']) * 100
            
            # Create analysis results dictionary
            analysis = {
                "summary": {
                    "latest_year": df['date'].iloc[0] if 'date' in df.columns else None,
                    "latest_revenue": float(df['revenue'].iloc[0]) if 'revenue' in df.columns else None,
                    "latest_net_income": float(df['netIncome'].iloc[0]) if 'netIncome' in df.columns else None,
                },
                "growth": {
                    # Handle NaN values which can occur in growth calculations for the first period
                    "revenue_growth": float(df['revenue_growth'].iloc[0]) if 'revenue_growth' in df.columns and not pd.isna(df['revenue_growth'].iloc[0]) else None,
                    "net_income_growth": float(df['net_income_growth'].iloc[0]) if 'net_income_growth' in df.columns and not pd.isna(df['net_income_growth'].iloc[0]) else None
                },
                "margins": {
                    "gross_margin": float(df['gross_margin'].iloc[0]) if 'gross_margin' in df.columns else None,
                    "operating_margin": float(df['operating_margin'].iloc[0]) if 'operating_margin' in df.columns else None,
                    "profit_margin": float(df['profit_margin'].iloc[0]) if 'profit_margin' in df.columns else None
                },
                "trends": convert_numpy_types(df.head())  # Include recent records for trend analysis
            }
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing income statement: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
            
    # ... existing code for other analysis methods ...
    
    def comprehensive_analysis(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of financial data by combining analyses of
        different financial statements and indicators.
        
        This method orchestrates the analysis of multiple data sources:
        - Income statements
        - Balance sheets
        - Cash flow statements
        - Technical indicators
        - Company profile information
        
        Args:
            financial_data (dict): Complete financial data for a company including
                                  various statements and metrics
            
        Returns:
            dict: Comprehensive analysis results combining insights from all data sources
        """
        results = {}
        
        # Analyze income statement if available
        if "income_statement" in financial_data:
            results["income_analysis"] = self.analyze_income_statement(financial_data["income_statement"])
            
        # Analyze balance sheet if available
        if "balance_sheet" in financial_data:
            results["balance_sheet_analysis"] = self.analyze_balance_sheet(financial_data["balance_sheet"])
            
        # Analyze cash flow if available
        if "cash_flow" in financial_data:
            results["cash_flow_analysis"] = self.analyze_cash_flow(financial_data["cash_flow"])
            
        # Analyze technical indicators if available
        if "technical_indicators" in financial_data:
            results["technical_analysis"] = self.analyze_technical_data(financial_data["technical_indicators"])
            
        # Get company profile
        company_profile = None
        if "company_profile" in financial_data and financial_data["company_profile"]:
            if isinstance(financial_data["company_profile"], list) and len(financial_data["company_profile"]) > 0:
                company_profile = financial_data["company_profile"][0]
            else:
                company_profile = financial_data["company_profile"]
                
        # Add company summary
        if company_profile:
            results["company_summary"] = {
                "name": company_profile.get("companyName", ""),
                "sector": company_profile.get("sector", ""),
                "industry": company_profile.get("industry", ""),
                "market_cap": company_profile.get("mktCap", 0),
                "beta": company_profile.get("beta", 0),
                "price": company_profile.get("price", 0),
                "description": company_profile.get("description", "")
            }
            
        return results
import sys
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.data_transformer import clean_and_convert_numeric, convert_numpy_types

logger = logging.getLogger("Financial_Analyzer")

class FinancialAnalyzer:
    """Module for analyzing financial data."""
    
    def __init__(self):
        """Initialize the financial analyzer."""
        pass
        
    def analyze_income_statement(self, income_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze income statement data.
        
        Args:
            income_data (list): Income statement data
            
        Returns:
            dict: Income statement analysis results
        """
        try:
            # Convert to DataFrame for easier analysis
            if not income_data or not isinstance(income_data, list):
                return {"error": "Invalid income statement data"}
                
            df = pd.DataFrame(income_data)
            df = clean_and_convert_numeric(df)
            
            # Calculate growth rates
            if 'revenue' in df.columns:
                df['revenue_growth'] = df['revenue'].pct_change(-1) * 100  # Previous year growth
                
            if 'netIncome' in df.columns:
                df['net_income_growth'] = df['netIncome'].pct_change(-1) * 100
                
            if 'grossProfit' in df.columns and 'revenue' in df.columns:
                df['gross_margin'] = (df['grossProfit'] / df['revenue']) * 100
                
            if 'operatingIncome' in df.columns and 'revenue' in df.columns:
                df['operating_margin'] = (df['operatingIncome'] / df['revenue']) * 100
                
            if 'netIncome' in df.columns and 'revenue' in df.columns:
                df['profit_margin'] = (df['netIncome'] / df['revenue']) * 100
            
            # Create analysis results dictionary
            analysis = {
                "summary": {
                    "latest_year": df['date'].iloc[0] if 'date' in df.columns else None,
                    "latest_revenue": float(df['revenue'].iloc[0]) if 'revenue' in df.columns else None,
                    "latest_net_income": float(df['netIncome'].iloc[0]) if 'netIncome' in df.columns else None,
                },
                "growth": {
                    "revenue_growth": float(df['revenue_growth'].iloc[0]) if 'revenue_growth' in df.columns and not pd.isna(df['revenue_growth'].iloc[0]) else None,
                    "net_income_growth": float(df['net_income_growth'].iloc[0]) if 'net_income_growth' in df.columns and not pd.isna(df['net_income_growth'].iloc[0]) else None
                },
                "margins": {
                    "gross_margin": float(df['gross_margin'].iloc[0]) if 'gross_margin' in df.columns else None,
                    "operating_margin": float(df['operating_margin'].iloc[0]) if 'operating_margin' in df.columns else None,
                    "profit_margin": float(df['profit_margin'].iloc[0]) if 'profit_margin' in df.columns else None
                },
                "trends": convert_numpy_types(df.head())
            }
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing income statement: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
            
    def analyze_balance_sheet(self, balance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze balance sheet data.
        
        Args:
            balance_data (list): Balance sheet data
            
        Returns:
            dict: Balance sheet analysis results
        """
        try:
            # Convert to DataFrame for easier analysis
            if not balance_data or not isinstance(balance_data, list):
                return {"error": "Invalid balance sheet data"}
                
            df = pd.DataFrame(balance_data)
            df = clean_and_convert_numeric(df)
            
            # Calculate key ratios
            if 'totalCurrentAssets' in df.columns and 'totalCurrentLiabilities' in df.columns:
                df['current_ratio'] = df['totalCurrentAssets'] / df['totalCurrentLiabilities']
                
            if 'totalAssets' in df.columns and 'totalLiabilities' in df.columns:
                df['debt_to_assets'] = df['totalLiabilities'] / df['totalAssets']
                
            if 'totalAssets' in df.columns and 'totalStockholdersEquity' in df.columns:
                df['return_on_assets'] = df['totalStockholdersEquity'] / df['totalAssets']
                
            # Create analysis results dictionary
            analysis = {
                "summary": {
                    "latest_date": df['date'].iloc[0] if 'date' in df.columns else None,
                    "total_assets": float(df['totalAssets'].iloc[0]) if 'totalAssets' in df.columns else None,
                    "total_liabilities": float(df['totalLiabilities'].iloc[0]) if 'totalLiabilities' in df.columns else None,
                    "stockholders_equity": float(df['totalStockholdersEquity'].iloc[0]) if 'totalStockholdersEquity' in df.columns else None
                },
                "ratios": {
                    "current_ratio": float(df['current_ratio'].iloc[0]) if 'current_ratio' in df.columns else None,
                    "debt_to_assets": float(df['debt_to_assets'].iloc[0]) if 'debt_to_assets' in df.columns else None,
                    "return_on_assets": float(df['return_on_assets'].iloc[0]) if 'return_on_assets' in df.columns else None
                },
                "trends": convert_numpy_types(df.head())
            }
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing balance sheet: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
            
    def analyze_cash_flow(self, cash_flow_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze cash flow statement data.
        
        Args:
            cash_flow_data (list): Cash flow statement data
            
        Returns:
            dict: Cash flow analysis results
        """
        try:
            # Convert to DataFrame for easier analysis
            if not cash_flow_data or not isinstance(cash_flow_data, list):
                return {"error": "Invalid cash flow data"}
                
            df = pd.DataFrame(cash_flow_data)
            df = clean_and_convert_numeric(df)
            
            # Calculate key metrics
            if 'netCashProvidedByOperatingActivities' in df.columns:
                operating_cash = df['netCashProvidedByOperatingActivities']
            else:
                operating_cash = None
                
            if 'capitalExpenditure' in df.columns and operating_cash is not None:
                df['free_cash_flow'] = operating_cash - df['capitalExpenditure']
                
            # Create analysis results dictionary
            analysis = {
                "summary": {
                    "latest_date": df['date'].iloc[0] if 'date' in df.columns else None,
                    "operating_cash_flow": float(df['netCashProvidedByOperatingActivities'].iloc[0]) 
                        if 'netCashProvidedByOperatingActivities' in df.columns else None,
                    "investing_cash_flow": float(df['netCashUsedForInvestingActivites'].iloc[0]) 
                        if 'netCashUsedForInvestingActivites' in df.columns else None,
                    "financing_cash_flow": float(df['netCashUsedProvidedByFinancingActivities'].iloc[0]) 
                        if 'netCashUsedProvidedByFinancingActivities' in df.columns else None
                },
                "metrics": {
                    "free_cash_flow": float(df['free_cash_flow'].iloc[0]) if 'free_cash_flow' in df.columns else None,
                    "capital_expenditure": float(df['capitalExpenditure'].iloc[0]) if 'capitalExpenditure' in df.columns else None
                },
                "trends": convert_numpy_types(df.head())
            }
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing cash flow: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
            
    def analyze_technical_data(self, technical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze technical indicators data.
        
        Args:
            technical_data (dict): Technical indicators data
            
        Returns:
            dict: Technical analysis results
        """
        analysis = {}
        
        for indicator, data in technical_data.items():
            if 'error' in data:
                analysis[indicator] = {"error": data["error"]}
                continue
                
            try:
                # Convert to DataFrame if applicable
                if isinstance(data, dict) and "historical" in data:
                    indicator_data = data["historical"]
                    if indicator_data and isinstance(indicator_data, list):
                        df = pd.DataFrame(indicator_data)
                        df = clean_and_convert_numeric(df)
                        
                        # Get recent values
                        recent_values = df.head()
                        
                        # Calculate average
                        value_col = next((col for col in df.columns if col not in ['date', 'symbol']), None)
                        avg_value = df[value_col].mean() if value_col else None
                        
                        analysis[indicator] = {
                            "latest_value": float(recent_values[value_col].iloc[0]) if value_col else None,
                            "average_value": float(avg_value) if avg_value is not None else None,
                            "recent_trend": "up" if len(recent_values) > 1 and 
                                             value_col and 
                                             recent_values[value_col].iloc[0] > recent_values[value_col].iloc[-1] 
                                          else "down",
                            "recent_values": convert_numpy_types(recent_values)
                        }
                    else:
                        analysis[indicator] = {"error": "No historical data available"}
                else:
                    analysis[indicator] = {"error": "Invalid data format"}
            except Exception as e:
                analysis[indicator] = {"error": f"Analysis failed: {str(e)}"}
        
        return analysis
    
    def comprehensive_analysis(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of financial data.
        
        Args:
            financial_data (dict): Complete financial data for a company
            
        Returns:
            dict: Comprehensive analysis results
        """
        results = {}
        
        # Analyze income statement if available
        if "income_statement" in financial_data:
            results["income_analysis"] = self.analyze_income_statement(financial_data["income_statement"])
            
        # Analyze balance sheet if available
        if "balance_sheet" in financial_data:
            results["balance_sheet_analysis"] = self.analyze_balance_sheet(financial_data["balance_sheet"])
            
        # Analyze cash flow if available
        if "cash_flow" in financial_data:
            results["cash_flow_analysis"] = self.analyze_cash_flow(financial_data["cash_flow"])
            
        # Analyze technical indicators if available
        if "technical_indicators" in financial_data:
            results["technical_analysis"] = self.analyze_technical_data(financial_data["technical_indicators"])
            
        # Get company profile
        company_profile = None
        if "company_profile" in financial_data and financial_data["company_profile"]:
            if isinstance(financial_data["company_profile"], list) and len(financial_data["company_profile"]) > 0:
                company_profile = financial_data["company_profile"][0]
            else:
                company_profile = financial_data["company_profile"]
                
        # Add company summary
        if company_profile:
            results["company_summary"] = {
                "name": company_profile.get("companyName", ""),
                "sector": company_profile.get("sector", ""),
                "industry": company_profile.get("industry", ""),
                "market_cap": company_profile.get("mktCap", 0),
                "beta": company_profile.get("beta", 0),
                "price": company_profile.get("price", 0),
                "description": company_profile.get("description", "")
            }
            
        return results
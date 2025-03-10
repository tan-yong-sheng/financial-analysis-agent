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
        
    def _ensure_json_serializable(self, data):
        """
        Ensure all values in the data structure are JSON serializable.
        Converts pandas Timestamp objects to ISO format strings.
        
        Args:
            data: Data structure (dict, list, or DataFrame) to convert
            
        Returns:
            Data structure with all values converted to JSON serializable types
        """
        if isinstance(data, dict):
            return {k: self._ensure_json_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._ensure_json_serializable(item) for item in data]
        elif isinstance(data, pd.DataFrame):
            # Convert DataFrame to dict first, then ensure all values are serializable
            df_dict = data.to_dict(orient='records')
            return self._ensure_json_serializable(df_dict)
        elif isinstance(data, pd.Timestamp):
            return data.isoformat()
        else:
            return data
            
    def analyze_income_statement(self, income_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze income statement data to extract revenue trends, profitability metrics, and growth rates.
        
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
            
            # Print debugging information to understand the actual data
            print(f"Columns in income statement: {df.columns.tolist()}")
            
            df = clean_and_convert_numeric(df)
            
            # Debug Boolean context issues by using explicit checks
            has_revenue = 'revenue' in df.columns
            has_net_income = 'netIncome' in df.columns
            has_gross_profit = 'grossProfit' in df.columns
            has_operating_income = 'operatingIncome' in df.columns
            
            # Fix for test data - convert columns to lowercase if needed
            if not has_revenue and 'Revenue' in df.columns:
                df.rename(columns={'Revenue': 'revenue'}, inplace=True)
                has_revenue = True
                
            if not has_net_income and 'Net Income' in df.columns:
                df.rename(columns={'Net Income': 'netIncome'}, inplace=True)
                has_net_income = True
                
            # Calculate growth rates
            if has_revenue:
                # Calculate YoY revenue growth (negative index because data is typically in reverse chronological order)
                df['revenue_growth'] = df['revenue'].pct_change(-1) * 100
                
            if has_net_income:
                # Calculate YoY net income growth
                df['net_income_growth'] = df['netIncome'].pct_change(-1) * 100
                
            # Calculate profit margins
            if has_gross_profit and has_revenue:
                # Gross margin = Gross profit / Revenue
                df['gross_margin'] = (df['grossProfit'] / df['revenue']) * 100
                
            if has_operating_income and has_revenue:
                # Operating margin = Operating income / Revenue
                df['operating_margin'] = (df['operatingIncome'] / df['revenue']) * 100
                
            if has_net_income and has_revenue:
                # Net profit margin = Net income / Revenue
                df['profit_margin'] = (df['netIncome'] / df['revenue']) * 100
            
            # Create analysis results dictionary
            analysis = {
                "summary": {
                    "latest_year": df['date'].iloc[0] if 'date' in df.columns else None,
                    "latest_revenue": float(df['revenue'].iloc[0]) if has_revenue else None,
                    "latest_net_income": float(df['netIncome'].iloc[0]) if has_net_income else None,
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
                "trends": convert_numpy_types(df.head(3).to_dict())  # Include recent records for trend analysis
            }
            
            # Ensure all values are JSON serializable
            return self._ensure_json_serializable(analysis)
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
            
            # Debug Boolean context issues by using explicit checks
            has_total_current_assets = 'totalCurrentAssets' in df.columns
            has_total_current_liabilities = 'totalCurrentLiabilities' in df.columns
            has_total_assets = 'totalAssets' in df.columns
            has_total_liabilities = 'totalLiabilities' in df.columns
            has_stockholders_equity = 'totalStockholdersEquity' in df.columns
            
            # Calculate key ratios with explicit checks
            if has_total_current_assets and has_total_current_liabilities:
                df['current_ratio'] = df['totalCurrentAssets'] / df['totalCurrentLiabilities']
                
            if has_total_assets and has_total_liabilities:
                df['debt_to_assets'] = df['totalLiabilities'] / df['totalAssets']
                
            if has_total_assets and has_stockholders_equity:
                df['return_on_assets'] = df['totalStockholdersEquity'] / df['totalAssets']
                
            # Create analysis results dictionary
            analysis = {
                "summary": {
                    "latest_date": df['date'].iloc[0] if 'date' in df.columns else None,
                    "total_assets": float(df['totalAssets'].iloc[0]) if has_total_assets else None,
                    "total_liabilities": float(df['totalLiabilities'].iloc[0]) if has_total_liabilities else None,
                    "stockholders_equity": float(df['totalStockholdersEquity'].iloc[0]) if has_stockholders_equity else None
                },
                "ratios": {
                    "current_ratio": float(df['current_ratio'].iloc[0]) if 'current_ratio' in df.columns else None,
                    "debt_to_assets": float(df['debt_to_assets'].iloc[0]) if 'debt_to_assets' in df.columns else None,
                    "return_on_assets": float(df['return_on_assets'].iloc[0]) if 'return_on_assets' in df.columns else None
                },
                "trends": convert_numpy_types(df.head().to_dict('records'))  # Convert directly to records to avoid DataFrame issues
            }
            
            return self._ensure_json_serializable(analysis)
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
            
            # Debug Boolean context issues by using explicit checks
            has_op_cash = 'netCashProvidedByOperatingActivities' in df.columns
            has_inv_cash = 'netCashUsedForInvestingActivites' in df.columns
            has_fin_cash = 'netCashUsedProvidedByFinancingActivities' in df.columns
            has_capex = 'capitalExpenditure' in df.columns
            
            # Calculate key metrics - only if necessary columns exist
            if has_op_cash and has_capex:
                df['free_cash_flow'] = df['netCashProvidedByOperatingActivities'] - df['capitalExpenditure']
                
            # Create analysis results dictionary
            analysis = {
                "summary": {
                    "latest_date": df['date'].iloc[0] if 'date' in df.columns else None,
                    "operating_cash_flow": float(df['netCashProvidedByOperatingActivities'].iloc[0]) 
                        if has_op_cash else None,
                    "investing_cash_flow": float(df['netCashUsedForInvestingActivites'].iloc[0]) 
                        if has_inv_cash else None,
                    "financing_cash_flow": float(df['netCashUsedProvidedByFinancingActivities'].iloc[0]) 
                        if has_fin_cash else None
                },
                "metrics": {
                    "free_cash_flow": float(df['free_cash_flow'].iloc[0]) if 'free_cash_flow' in df.columns else None,
                    "capital_expenditure": float(df['capitalExpenditure'].iloc[0]) if has_capex else None
                },
                "trends": convert_numpy_types(df.head().to_dict('records'))  # Convert to records format directly
            }
            
            return self._ensure_json_serializable(analysis)
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
        
        # Handle the case where technical_data might be None or invalid
        if not technical_data or not isinstance(technical_data, dict):
            return {"error": "Invalid technical data"}
            
        # Print debug info to understand the structure
        print(f"Technical data keys: {list(technical_data.keys())}")
        
        for indicator, data in technical_data.items():
            if isinstance(data, dict) and 'error' in data:
                analysis[indicator] = {"error": data["error"]}
                continue
                
            try:
                # Convert to DataFrame if applicable
                if isinstance(data, dict) and "historical" in data:
                    indicator_data = data["historical"]
                    # Print more debug info
                    print(f"Indicator data for {indicator}: {indicator_data[:2] if indicator_data else []}")
                    
                    if indicator_data and isinstance(indicator_data, list) and len(indicator_data) > 0:
                        df = pd.DataFrame(indicator_data)
                        df = clean_and_convert_numeric(df)
                        
                        # Get recent values
                        recent_values = df.head()
                        
                        # Calculate average - fix boolean context issues
                        # Find the value column (not date or symbol)
                        value_cols = [col for col in df.columns if col not in ['date', 'symbol']]
                        if len(value_cols) > 0:
                            value_col = value_cols[0]
                            avg_value = df[value_col].mean() if len(df) > 0 else None
                            
                            # Ensure there are values to use
                            if len(recent_values) > 0:
                                latest_value = float(recent_values[value_col].iloc[0])
                                trend_direction = "up"
                                if len(recent_values) > 1:
                                    trend_direction = "up" if latest_value > float(recent_values[value_col].iloc[-1]) else "down"
                                    
                                analysis[indicator] = {
                                    "latest_value": latest_value,
                                    "average_value": float(avg_value) if avg_value is not None else None,
                                    "recent_trend": trend_direction,
                                    # Convert to dict instead of DataFrame to avoid serialization issues
                                    "recent_values": convert_numpy_types(recent_values.to_dict('records'))
                                }
                            else:
                                analysis[indicator] = {"error": "No values available"}
                        else:
                            analysis[indicator] = {"error": "No value column found"}
                    else:
                        analysis[indicator] = {"error": "No historical data available"}
                else:
                    analysis[indicator] = {"error": "Invalid data format"}
            except Exception as e:
                print(f"Error processing {indicator}: {str(e)}")
                analysis[indicator] = {"error": f"Analysis failed: {str(e)}"}
        
        return self._ensure_json_serializable(analysis)
    
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
            
        return self._ensure_json_serializable(results)
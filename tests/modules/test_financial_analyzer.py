import pytest
import pandas as pd
import numpy as np
import json  # Add missing import
from modules.financial_analyzer import FinancialAnalyzer

class TestFinancialAnalyzer:
    """Tests for the FinancialAnalyzer module."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.analyzer = FinancialAnalyzer()
    
    def test_analyze_income_statement(self, sample_income_statement):
        """Test income statement analysis."""
        # Call the method under test
        result = self.analyzer.analyze_income_statement(sample_income_statement)
        
        # Assertions
        assert "summary" in result
        assert "growth" in result
        assert "margins" in result
        assert result["summary"]["latest_revenue"] == 1000000
        assert result["summary"]["latest_net_income"] == 200000
        
        # Check calculated metrics (revenue growth from 900k to 1000k)
        assert abs(result["growth"]["revenue_growth"] - 11.11) < 0.1  # ~11.11% growth
        
        # Check margin calculations
        assert abs(result["margins"]["gross_margin"] - 60.0) < 0.1  # 60% gross margin
        assert abs(result["margins"]["profit_margin"] - 20.0) < 0.1  # 20% profit margin
    
    def test_analyze_balance_sheet(self, sample_balance_sheet):
        """Test balance sheet analysis."""
        result = self.analyzer.analyze_balance_sheet(sample_balance_sheet)
        
        # Assertions
        assert "summary" in result
        assert "ratios" in result
        assert result["summary"]["total_assets"] == 2000000
        
        # Check calculated ratios
        assert abs(result["ratios"]["current_ratio"] - 1.4) < 0.1  # Current ratio = 700k/500k = 1.4
        assert abs(result["ratios"]["debt_to_assets"] - 0.4) < 0.1  # Debt to assets = 800k/2000k = 0.4
    
    def test_analyze_cash_flow(self, sample_cash_flow):
        """Test cash flow analysis."""
        result = self.analyzer.analyze_cash_flow(sample_cash_flow)
        
        # Assertions
        assert "summary" in result
        assert "metrics" in result
        assert result["summary"]["operating_cash_flow"] == 250000
        
        # Check calculated free cash flow (operating cash - capex)
        assert result["metrics"]["free_cash_flow"] == 175000  # 250k - 75k
    
    def test_analyze_technical_data(self, sample_technical_data):
        """Test technical data analysis."""
        result = self.analyzer.analyze_technical_data(sample_technical_data)
        
        # Assertions
        assert "rsi" in result
        assert "macd" in result
        assert result["rsi"]["latest_value"] == 65.5
        assert result["macd"]["latest_value"] == 2.5
        
        # Check trend calculation
        assert result["rsi"]["recent_trend"] == "up"  # 65.5 > 64.2
    
    def test_comprehensive_analysis(self, sample_financial_data):
        """Test the comprehensive analysis function."""
        result = self.analyzer.comprehensive_analysis(sample_financial_data)
        
        # Assertions for presence of all analysis components
        assert "income_analysis" in result
        assert "balance_sheet_analysis" in result
        assert "cash_flow_analysis" in result
        assert "technical_analysis" in result
        assert "company_summary" in result
        
        # Check that company summary is properly extracted
        assert result["company_summary"]["name"] == "Test Company"
        assert result["company_summary"]["sector"] == "Technology"
    
    def test_handle_empty_data(self):
        """Test handling of empty or invalid data."""
        # Empty income statement
        assert "error" in self.analyzer.analyze_income_statement([])
        
        # None data
        assert "error" in self.analyzer.analyze_balance_sheet(None)
        
        # Invalid data type
        assert "error" in self.analyzer.analyze_cash_flow("not a list")
    
    def test_serializable_output(self, sample_financial_data):
        """Test that all outputs are JSON serializable."""
        result = self.analyzer.comprehensive_analysis(sample_financial_data)
        
        # Should not raise any exception
        json_str = json.dumps(result)
        assert isinstance(json_str, str)

import pytest
import pandas as pd
import numpy as np
import json
import os
from unittest.mock import MagicMock, patch

@pytest.fixture
def sample_income_statement():
    """Sample income statement data for testing."""
    return [
        {
            "date": "2023-12-31",
            "revenue": 1000000,
            "grossProfit": 600000,
            "operatingIncome": 300000,
            "netIncome": 200000
        },
        {
            "date": "2022-12-31",
            "revenue": 900000,
            "grossProfit": 540000,
            "operatingIncome": 270000,
            "netIncome": 180000
        }
    ]

@pytest.fixture
def sample_balance_sheet():
    """Sample balance sheet data for testing."""
    return [
        {
            "date": "2023-12-31",
            "totalAssets": 2000000,
            "totalLiabilities": 800000,
            "totalCurrentAssets": 700000,
            "totalCurrentLiabilities": 500000,
            "totalStockholdersEquity": 1200000
        },
        {
            "date": "2022-12-31",
            "totalAssets": 1800000,
            "totalLiabilities": 700000,
            "totalCurrentAssets": 600000,
            "totalCurrentLiabilities": 450000,
            "totalStockholdersEquity": 1100000
        }
    ]

@pytest.fixture
def sample_cash_flow():
    """Sample cash flow data for testing."""
    return [
        {
            "date": "2023-12-31",
            "netCashProvidedByOperatingActivities": 250000,
            "netCashUsedForInvestingActivites": -80000,
            "netCashUsedProvidedByFinancingActivities": -100000,
            "capitalExpenditure": 75000
        },
        {
            "date": "2022-12-31",
            "netCashProvidedByOperatingActivities": 220000,
            "netCashUsedForInvestingActivites": -70000,
            "netCashUsedProvidedByFinancingActivities": -90000,
            "capitalExpenditure": 65000
        }
    ]

@pytest.fixture
def sample_technical_data():
    """Sample technical indicator data for testing."""
    return {
        "rsi": {
            "historical": [
                {"date": "2023-12-31", "value": 65.5},
                {"date": "2023-12-30", "value": 64.2}
            ]
        }
    }

@pytest.fixture
def sample_company_profile():
    """Sample company profile data for testing."""
    return {
        "companyName": "Test Company",
        "sector": "Technology",
        "industry": "Software",
        "mktCap": 10000000000,
        "beta": 1.2,
        "price": 150.0,
        "description": "A test company description."
    }

@pytest.fixture
def sample_financial_data(sample_income_statement, sample_balance_sheet, 
                         sample_cash_flow, sample_technical_data, sample_company_profile):
    """Combined financial data for testing."""
    return {
        "income_statement": sample_income_statement,
        "balance_sheet": sample_balance_sheet,
        "cash_flow": sample_cash_flow,
        "technical_indicators": sample_technical_data,
        "company_profile": sample_company_profile
    }

@pytest.fixture
def mock_llm_response():
    """Mock LLM response for agent testing."""
    return MagicMock(return_value=json.dumps({
        "analysis": "This is a mock analysis",
        "recommendation": "Buy",
        "key_metrics": {"revenue_growth": "11.1%", "profit_margin": "20%"}
    }))

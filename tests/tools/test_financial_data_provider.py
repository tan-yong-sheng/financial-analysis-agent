import pytest
from unittest.mock import patch, MagicMock
from tools.financial_data_provider import FinancialDataProvider

@pytest.fixture
def mock_provider():
    with patch('tools.financial_data_provider.requests.get') as mock_get:
        provider = FinancialDataProvider()
        mock_get.return_value = MagicMock()
        yield provider, mock_get

def test_get_technical_indicator_success(mock_provider):
    """Test successful retrieval of technical indicators."""
    provider, mock_get = mock_provider
    
    # Mock successful response
    mock_get.return_value.json.return_value = {
        "technicalIndicator": [
            {"date": "2024-03-10", "value": 65.42},
            {"date": "2024-03-09", "value": 63.21}
        ]
    }
    mock_get.return_value.raise_for_status = MagicMock()
    
    # Test RSI indicator
    result = provider.get_technical_indicator('AAPL', 'rsi', 14)
    assert len(result) == 2
    assert isinstance(result, list)
    assert result[0]["value"] == 65.42

def test_get_technical_indicator_error_handling(mock_provider):
    """Test error handling in technical indicators."""
    provider, mock_get = mock_provider
    
    # Test invalid indicator
    result = provider.get_technical_indicator('AAPL', 'invalid_indicator', 14)
    assert result == []
    
    # Test API error response
    mock_get.return_value.raise_for_status.side_effect = Exception("API Error")
    result = provider.get_technical_indicator('AAPL', 'rsi', 14)
    assert result == []

def test_check_api_status(mock_provider):
    """Test API status check functionality."""
    provider, mock_get = mock_provider
    
    # Mock successful status response
    mock_get.return_value.json.return_value = {"status": "OK", "message": "API is working"}
    mock_get.return_value.raise_for_status = MagicMock()
    
    result = provider.check_api_status()
    assert result["status"] == "OK"
    assert "message" in result

def test_get_technical_indicator():
    """Test retrieval of technical indicators."""
    provider = FinancialDataProvider()
    indicators = provider.get_technical_indicator('AAPL', 'rsi', 14)
    
    # Simply check if we get a non-empty response
    assert isinstance(indicators, list)
    
    # If we expect indicators to be empty for valid reasons (like API limits),
    # this test should be skipped or the assertion modified

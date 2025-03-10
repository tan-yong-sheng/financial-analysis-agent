import pytest
from unittest.mock import patch, MagicMock
import json
import requests
from agents.data_collection_agent import DataCollectionAgent

class TestDataCollectionAgent:
    """Tests for the DataCollectionAgent."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.agent = DataCollectionAgent(base_url="mock_url", model_name="mock_model")
    
    @patch('agents.data_collection_agent.requests.get')
    def test_get_company_profile_success(self, mock_get):
        """Test successful company profile retrieval."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [{
            "companyName": "Test Company",
            "sector": "Technology",
            "industry": "Software"
        }]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.agent.get_company_profile("TEST")
        
        # Assertions
        assert result["companyName"] == "Test Company"
        assert result["sector"] == "Technology"
        assert result["industry"] == "Software"
        
        # Verify API call
        mock_get.assert_called_once_with(f"{self.agent.base_url}/profile/TEST?apikey={self.agent.api_key}")
    
    @patch('agents.data_collection_agent.requests.get')
    def test_get_company_profile_empty_response(self, mock_get):
        """Test empty response handling."""
        # Setup mock to return empty list
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.agent.get_company_profile("TEST")
        
        # Assertions - should return error dict
        assert "error" in result
        assert "No company profile found" in result["error"]
    
    @patch('agents.data_collection_agent.requests.get')
    def test_get_company_profile_api_error(self, mock_get):
        """Test API error handling."""
        # Setup mock to raise exception
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        # Call the method
        result = self.agent.get_company_profile("TEST")
        
        # Assertions - should return error dict
        assert "error" in result
        assert "Failed to fetch company profile" in result["error"]
    
    @patch('agents.data_collection_agent.requests.get')
    def test_get_income_statement(self, mock_get):
        """Test income statement retrieval."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [{"revenue": 1000000}, {"revenue": 900000}]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.agent.get_income_statement("TEST")
        
        # Assertions
        assert len(result) == 2
        assert result[0]["revenue"] == 1000000
        assert result[1]["revenue"] == 900000

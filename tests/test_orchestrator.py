import pytest
from unittest.mock import patch, MagicMock, mock_open as mock_open_func
import os
import json
from orchestrator import FinancialAnalysisOrchestrator

class TestOrchestrator:
    """Tests for the main orchestrator."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.orchestrator = FinancialAnalysisOrchestrator()
    
    @patch('orchestrator.FinancialAnalysisOrchestrator._get_initial_company_data')
    @patch('orchestrator.FinancialAnalysisOrchestrator._create_research_plan')
    @patch('orchestrator.FinancialAnalysisOrchestrator._collect_financial_data')
    @patch('orchestrator.FinancialAnalysisOrchestrator._conduct_market_research')
    @patch('orchestrator.FinancialAnalysisOrchestrator._analyze_data_and_research')
    @patch('agents.report_agent.ReportAgent.process')
    @patch('builtins.open', new_callable=mock_open_func)
    @patch('json.dump')
    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_analyze_company(self, mock_exists, mock_makedirs, mock_json_dump, 
                            mock_file, mock_report_process, mock_analyze, 
                            mock_research, mock_collect_data, mock_plan, mock_initial_data):
        """Test the main analyze_company workflow."""
        # Setup mocks
        mock_initial_data.return_value = {"name": "Test Company"}
        mock_plan.return_value = {"key_areas": ["financials", "competition"]}
        mock_collect_data.return_value = {"financial_data": "test"}
        mock_research.return_value = {"research_results": "test"}
        mock_analyze.return_value = {"analysis_results": "test"}
        mock_exists.return_value = False
        mock_report_process.return_value = {
            "ticker": "TEST",
            "report": "Test report content",
            "report_file_path": "reports/TEST_analysis.md"
        }
        
        # Run the method
        result = self.orchestrator.analyze_company("TEST")
        
        # Verify all steps were called in sequence
        mock_initial_data.assert_called_once_with("TEST")
        mock_plan.assert_called_once()
        mock_collect_data.assert_called_once()
        mock_research.assert_called_once()
        mock_analyze.assert_called_once()
        
        # Verify os.path.exists and directories were checked/created
        mock_exists.assert_called()
        mock_makedirs.assert_called()
        
        # Verify file operations occurred
        assert mock_file.call_count >= 1
        mock_json_dump.assert_called_once()
        
        # Check return values 
        assert "execution_time" in result
        assert "report_path" in result
        assert result["ticker"] == "TEST"

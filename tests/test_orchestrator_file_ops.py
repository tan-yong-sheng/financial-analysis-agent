import pytest
from unittest.mock import patch, MagicMock, mock_open as mock_open_func
import os
import json
from orchestrator import FinancialAnalysisOrchestrator

class TestOrchestratorFileOperations:
    """Tests for file operation methods in the Orchestrator."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.orchestrator = FinancialAnalysisOrchestrator()
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open_func)
    @patch('json.dump')
    @patch('agents.report_agent.ReportAgent.process')
    def test_write_output_files(self, mock_report_process, mock_json_dump, mock_open, 
                               mock_makedirs, mock_exists):
        """Test writing output files and directory creation."""
        # Setup mocks
        mock_exists.return_value = False  # Directory doesn't exist
        mock_report_process.return_value = {
            "ticker": "TEST",
            "report": "Test report content",
            "report_file_path": "reports/TEST_analysis.md"
        }
        analysis_results = {"test": "data"}
        
        # Call the method
        self.orchestrator._write_output_files("TEST", analysis_results)
        
        # Verify directory check and creation
        mock_exists.assert_called_once_with("reports")
        mock_makedirs.assert_called_once_with("reports", exist_ok=True)
        
        # Verify files were written
        assert mock_open.call_count == 2  # One for MD report, one for JSON
        mock_json_dump.assert_called_once_with(analysis_results, mock_open.return_value.__enter__.return_value, indent=2)
        
        # Test the case where directory exists
        mock_exists.reset_mock()
        mock_makedirs.reset_mock()
        mock_open.reset_mock()
        mock_json_dump.reset_mock()
        
        mock_exists.return_value = True  # Directory exists
        
        # Call the method again
        self.orchestrator._write_output_files("TEST", analysis_results)
        
        # Directory check still happens but makedirs shouldn't be called
        mock_exists.assert_called_once()
        mock_makedirs.assert_not_called()

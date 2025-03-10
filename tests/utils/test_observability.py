import pytest
import json
import logging
from unittest.mock import MagicMock, patch
from utils.observability import StructuredLogger, log_execution_time, monitor_agent_method, AgentTracer

class TestStructuredLogger:
    """Test cases for StructuredLogger class."""
    
    @pytest.fixture
    def mock_logger(self):
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            yield mock_logger
    
    def test_structured_logger_initialization(self, mock_logger):
        """Test StructuredLogger initialization."""
        logger = StructuredLogger("test_logger", logging.INFO)
        assert logger.context == {}
        mock_logger.setLevel.assert_called_once_with(logging.INFO)
    
    def test_structured_logger_set_context(self, mock_logger):
        """Test setting context in StructuredLogger."""
        logger = StructuredLogger("test_logger")
        logger.set_context(app="test_app", env="test")
        assert logger.context == {"app": "test_app", "env": "test"}
        
        # Update existing context
        logger.set_context(app="new_app")
        assert logger.context == {"app": "new_app", "env": "test"}
    
    def test_structured_logger_log_method(self, mock_logger):
        """Test _log method correctly formats messages."""
        logger = StructuredLogger("test_logger")
        logger.context = {"app": "test_app"}
        
        # Log a message with additional context
        logger._log(logging.INFO, "Test message", user="test_user")
        
        # Verify the logger was called with the correct JSON string
        mock_logger.log.assert_called_once()
        args = mock_logger.log.call_args[0]
        assert args[0] == logging.INFO
        
        # Parse the JSON string to verify structure
        log_data = json.loads(args[1])
        assert log_data["message"] == "Test message"
        assert log_data["app"] == "test_app"
        assert log_data["user"] == "test_user"
        assert "timestamp" in log_data
    
    def test_log_methods(self, mock_logger):
        """Test the different log level methods."""
        logger = StructuredLogger("test_logger")
        
        logger.info("Info message", key="value")
        logger.error("Error message", error_code=500)
        logger.warning("Warning message")
        logger.debug("Debug message")
        logger.critical("Critical message")
        
        assert mock_logger.log.call_count == 5

class TestAgentTracer:
    """Test cases for AgentTracer class."""
    
    @pytest.fixture
    def mock_structured_logger(self):
        return MagicMock(spec=StructuredLogger)
    
    def test_agent_tracer_start_task(self, mock_structured_logger):
        """Test starting a task with AgentTracer."""
        tracer = AgentTracer("TestAgent", mock_structured_logger)
        tracer.start_task("test_task", param="value")
        
        mock_structured_logger.info.assert_called_once()
        args, kwargs = mock_structured_logger.info.call_args
        assert "started task" in args[0]
        assert kwargs["agent"] == "TestAgent"
        assert kwargs["task"] == "test_task"
        assert kwargs["event"] == "task_start"
        assert kwargs["param"] == "value"
    
    def test_agent_tracer_end_task(self, mock_structured_logger):
        """Test ending a task with AgentTracer."""
        tracer = AgentTracer("TestAgent", mock_structured_logger)
        tracer.current_task = "test_task"
        tracer.task_start_time = 12345.0
        
        result_summary = {"status": "success"}
        tracer.end_task(status="completed", result_summary=result_summary)
        
        mock_structured_logger.info.assert_called_once()
        args, kwargs = mock_structured_logger.info.call_args
        assert "completed task" in args[0]
        assert kwargs["agent"] == "TestAgent"
        assert kwargs["task"] == "test_task"
        assert kwargs["event"] == "task_end"
        assert kwargs["status"] == "completed"
        assert kwargs["result"] == result_summary

def test_monitor_agent_method():
    """Test monitor_agent_method decorator works correctly."""
    
    @monitor_agent_method()
    def test_function(self, param):
        return {"result": param}
    
    # Create a simple object to use as self
    obj = type('TestObject', (), {'name': 'TestAgent'})()
    
    # Execute the decorated function
    with patch('utils.observability.StructuredLogger') as mock_structured_logger_class:
        mock_logger_instance = MagicMock()
        mock_structured_logger_class.return_value = mock_logger_instance
        
        result = test_function(obj, "test_param")
        
        # Assert function returned expected result
        assert result == {"result": "test_param"}
        
        # Assert logger was created with expected name
        mock_structured_logger_class.assert_called_once()
        assert "TestAgent" in mock_structured_logger_class.call_args[0][0]
        
        # Assert start and end log messages were made
        assert mock_logger_instance.info.call_count == 2
        assert "Starting" in mock_logger_instance.info.call_args_list[0][0][0]
        assert "Completed" in mock_logger_instance.info.call_args_list[1][0][0]

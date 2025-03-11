# Writing Tests

This guide explains how to write tests for different components of the Financial Analysis System.

## Testing Framework

The system uses Python's `unittest` framework along with `pytest` for testing. Key testing utilities are provided in `tests/conftest.py`, including fixtures for sample data and mock responses.

## Test Structure

Tests are organized by component type in the `tests` directory:
```
tests/
├── agents/        # Tests for agent classes
├── models/        # Tests for data models
├── modules/       # Tests for core modules
├── tools/         # Tests for utility tools
├── utils/         # Tests for utilities
└── conftest.py    # Shared test fixtures
```

## Writing Tests for New Components

### Testing Agents

When adding a new agent, create a test file in `tests/agents/`. Agent tests should:

1. Test initialization
2. Test LLM interactions (using mocks)
3. Test the process method
4. Test error handling

Example:
```python
import pytest
from unittest.mock import Mock, patch
from agents.my_new_agent import MyNewAgent

class TestMyNewAgent:
    def setup_method(self):
        """Setup for each test."""
        self.agent = MyNewAgent()

    @patch('agents.base_agent.BaseAgent._call_llm')
    def test_process_method(self, mock_llm):
        """Test the main process method."""
        # Setup the mock LLM response
        mock_llm.return_value = '{"key": "test response"}'
        
        # Prepare test input
        test_input = {"data": "test"}
        
        # Call the method
        result = self.agent.process(test_input)
        
        # Verify the result
        assert "key" in result
        assert result["key"] == "test response"
        
        # Verify LLM was called correctly
        mock_llm.assert_called_once()

    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            self.agent.process(None)
```

### Testing Modules

For new modules, create tests in `tests/modules/`. Module tests should focus on:

1. Data processing logic
2. Calculations
3. Input validation
4. Edge cases

Example:
```python
import pytest
from modules.my_new_module import MyNewModule

class TestMyNewModule:
    def setup_method(self):
        self.module = MyNewModule()
        
    def test_calculations(self, sample_financial_data):
        """Test calculation methods using sample data fixture."""
        result = self.module.calculate_metrics(sample_financial_data)
        
        assert "metric_1" in result
        assert isinstance(result["metric_1"], float)
        assert result["metric_1"] >= 0
        
    def test_input_validation(self):
        """Test input validation."""
        with pytest.raises(ValueError):
            self.module.calculate_metrics({})  # Empty data
```

### Testing Tools

For new tools, create tests in `tests/tools/`. Tool tests should cover:

1. External API interactions (using mocks)
2. Data transformation
3. Error handling
4. Rate limiting/retry logic

Example:
```python
import pytest
from unittest.mock import patch
from tools.my_new_tool import MyNewTool

class TestMyNewTool:
    def setup_method(self):
        self.tool = MyNewTool()

    @patch('requests.get')
    def test_api_call(self, mock_get):
        """Test API interaction."""
        # Setup mock response
        mock_get.return_value.json.return_value = {"data": "test"}
        mock_get.return_value.status_code = 200
        
        result = self.tool.fetch_data("test_param")
        
        assert "data" in result
        mock_get.assert_called_once()
        
    @patch('requests.get')
    def test_rate_limiting(self, mock_get):
        """Test rate limit handling."""
        # Simulate rate limit response
        mock_get.return_value.status_code = 429
        
        with pytest.raises(RateLimitError):
            self.tool.fetch_data("test_param")
```

## Using Test Fixtures

The system provides common test fixtures in `conftest.py`. Use these to maintain consistency:

```python
def test_analysis(self, sample_financial_data, sample_company_profile):
    """Test using shared fixtures."""
    result = self.module.analyze(
        financial_data=sample_financial_data,
        company_info=sample_company_profile
    )
    # Assertions...
```

## Testing Observability

All components should include tests for their logging and monitoring:

```python
@patch('utils.observability.StructuredLogger')
def test_logging(self, mock_logger):
    """Test logging behavior."""
    self.component.process_data({"test": "data"})
    
    # Verify logs were created
    mock_logger.return_value.info.assert_called_with(
        "Processing completed",
        data_points=1,
        status="success"
    )
```

## Running Tests

Run the full test suite:
```bash
python -m pytest
```

Run tests with coverage:
```bash
python -m pytest --cov=.
```

Run specific tests:
```bash
python -m pytest tests/agents/test_my_agent.py
```

## Test Coverage Requirements

- All new components must have at least 80% test coverage
- Critical paths must have 100% coverage
- All error handling must be tested
- All public methods must have tests
- All logging/monitoring must be verified

## Best Practices

1. Use meaningful test names that describe the scenario
2. Test both success and failure cases
3. Use parameterized tests for testing multiple scenarios
4. Mock external dependencies and APIs
5. Test edge cases and boundary conditions
6. Verify logging and monitoring
7. Keep tests focused and independent
8. Use appropriate fixtures for common test data

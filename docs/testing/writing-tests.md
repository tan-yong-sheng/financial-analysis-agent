# Writing Tests

## Test Structure

All test files should follow this basic structure:

```python
import pytest
from unittest.mock import patch, MagicMock

class TestComponent:
    """Tests for the Component."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.component = Component()
    
    def test_specific_functionality(self):
        """Test description."""
        # Setup
        input_data = {...}
        
        # Execute
        result = self.component.method(input_data)
        
        # Assert
        assert result["expected_key"] == expected_value
```

## Using Fixtures

```python
def test_with_fixture(sample_financial_data):
    """Test using shared fixture."""
    result = analyze(sample_financial_data)
    assert "analysis" in result
```

## Mocking External Dependencies

```python
@patch('requests.get')
def test_api_call(mock_get):
    """Test API interaction."""
    mock_get.return_value.json.return_value = {"data": "test"}
    result = fetch_data()
    assert result["data"] == "test"
```

## Best Practices

1. **Test Names**: Use descriptive names that indicate what is being tested
2. **Assertions**: Make specific assertions that verify exact conditions
3. **Setup**: Use `setup_method` for common initialization
4. **Mocking**: Mock external dependencies to isolate tests
5. **Documentation**: Include docstrings explaining test purpose

# Implementing Logging

This guide explains how to implement logging in new components of the Financial Analysis System.

## Logging Architecture

The system uses structured logging with JSON output format for better observability. Logs are organized into different categories:

- Agent logs (agent activities and LLM interactions)
- API logs (external API calls and responses)
- Error logs (errors and exceptions)
- General logs (system-wide events)

## Directory Structure

Logs are stored in the `logs` directory with the following structure:
```
logs/
├── agents/     # Agent-specific logs
├── api/        # API interaction logs
├── errors/     # Error logs across all components
└── general/    # General application logs
```

## Setting Up Logging in New Components

### 1. Agent Implementation

When creating a new agent, inherit logging capabilities from BaseAgent:

```python
from utils.observability import StructuredLogger, monitor_agent_method
from agents.base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    """A new agent implementation."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        """Initialize with logging."""
        role = "specialist role description"
        super().__init__(role, "MyNewAgent", base_url=base_url, model_name=model_name)
        
    @monitor_agent_method()
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input with logging."""
        self.logger.info("Starting processing",
                        input_type=type(input_data).__name__)
        
        try:
            # Process the data...
            result = {"processed": "data"}
            
            self.logger.info("Processing completed",
                           output_size=len(result))
            return result
            
        except Exception as e:
            self.logger.error("Processing failed",
                            error_type=type(e).__name__,
                            error_message=str(e))
            raise
```

### 2. Module Implementation

For new modules, use StructuredLogger directly:

```python
from utils.observability import StructuredLogger

class MyNewModule:
    """A new module implementation."""
    
    def __init__(self):
        """Initialize with logging."""
        self.logger = StructuredLogger("my_new_module")
        
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data with logging."""
        start_time = time.time()
        self.logger.info("Starting data processing",
                        data_points=len(data))
        
        try:
            # Process the data...
            result = {"processed": "data"}
            
            execution_time = time.time() - start_time
            self.logger.info("Data processing completed",
                           execution_time=execution_time,
                           output_size=len(result))
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error("Data processing failed",
                            execution_time=execution_time,
                            error_type=type(e).__name__,
                            error_message=str(e))
            raise
```

### 3. Tool Implementation

For new tools, especially those interacting with external services:

```python
from utils.observability import StructuredLogger

class MyNewTool:
    """A new tool implementation."""
    
    def __init__(self):
        """Initialize with logging."""
        self.logger = StructuredLogger("my_new_tool")
        self.request_count = 0
        self.error_count = 0
        
    def make_external_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make external API call with logging."""
        start_time = time.time()
        self.request_count += 1
        
        self.logger.info("Making external API call",
                        request_number=self.request_count,
                        params=params)
        
        try:
            # Make the API call...
            response = requests.get("https://api.example.com", params=params)
            response.raise_for_status()
            
            execution_time = time.time() - start_time
            response_size = len(response.content)
            
            self.logger.info("API call successful",
                           status_code=response.status_code,
                           execution_time=execution_time,
                           response_size=response_size,
                           total_requests=self.request_count)
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.error_count += 1
            execution_time = time.time() - start_time
            
            self.logger.error("API call failed",
                            execution_time=execution_time,
                            error_count=self.error_count,
                            error_type=type(e).__name__,
                            error_message=str(e))
            raise
```

## Best Practices

1. **Structured Data**: Always pass structured data to log methods:
```python
# Good
logger.info("Processing started", input_size=len(data), data_type=type(data).__name__)

# Bad
logger.info(f"Processing started with {len(data)} items")
```

2. **Performance Metrics**: Include timing and size information:
```python
start_time = time.time()
# ... process ...
execution_time = time.time() - start_time
logger.info("Processing completed", execution_time=execution_time)
```

3. **Error Context**: Provide detailed error information:
```python
try:
    # ... code ...
except Exception as e:
    logger.error("Operation failed",
                error_type=type(e).__name__,
                error_message=str(e),
                stack_trace=traceback.format_exc())
    raise
```

4. **Sensitive Data**: Never log sensitive information:
```python
# Good
logger.info("API call", endpoint="user/profile", user_id=123)

# Bad
logger.info("API call", endpoint="user/profile", password="secret")
```

5. **Log Levels**:
- DEBUG: Detailed information for debugging
- INFO: General operational events
- WARNING: Unexpected but handled situations
- ERROR: Errors that need attention
- CRITICAL: System-level critical issues

6. **Method Monitoring**: Use the monitor_agent_method decorator:
```python
@monitor_agent_method()
def my_method(self, arg1, arg2):
    # Method code...
```

## Testing Logging

Always include tests for logging behavior:

```python
@patch('utils.observability.StructuredLogger')
def test_logging_behavior(self, mock_logger):
    component = MyNewComponent()
    component.process_data({"test": "data"})
    
    mock_logger.return_value.info.assert_called_with(
        "Processing completed",
        data_points=1,
        status="success"
    )
    
    # Test error logging
    with pytest.raises(ValueError):
        component.process_data(None)
        
    mock_logger.return_value.error.assert_called_with(
        "Processing failed",
        error_type="ValueError"
    )
```

## Log Analysis

Logs can be analyzed using standard tools:

```bash
# Search for errors
grep "level=ERROR" logs/errors/*.log

# Count API calls by endpoint
jq 'select(.endpoint) | .endpoint' logs/api/*.log | sort | uniq -c

# Calculate average execution time
jq 'select(.execution_time) | .execution_time' logs/general/*.log | \
    awk '{ sum += $1 } END { print sum/NR }'

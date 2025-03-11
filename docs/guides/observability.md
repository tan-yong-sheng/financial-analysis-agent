# Observability Guide

This guide covers the observability features in the Financial Analysis Agent system, including logging, tracing, and monitoring.

## Logging System

The system uses Python's standard logging module with structured logging enhancements:

```python
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Structured Logging

For complex operations, structured logging is used:

```python
from utils.observability import StructuredLogger

structured_logger = StructuredLogger("ResearchAgent")
structured_logger.info(
    event="research_started",
    ticker=ticker,
    research_areas=research_plan.get("key_areas", [])
)
```

This produces logs that can be easily parsed and analyzed:

```json
{
  "timestamp": "2023-05-15T10:30:45.123Z",
  "level": "INFO",
  "agent": "ResearchAgent",
  "event": "research_started",
  "ticker": "AAPL",
  "research_areas": ["financial_performance", "market_position", "industry_trends"],
  "message": "Started research for AAPL"
}
```

## Tracing

For complex operations that span multiple functions, the system uses tracing:

```python
@monitor_agent_method()
def create_research_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    self.tracer.start_task("create_research_plan", ticker=input_data.get("ticker"))
    try:
        # Implementation...
        self.tracer.end_task(status="success", result_summary={"ticker": result.get("ticker")})
        return result
    except Exception as e:
        self.tracer.end_task(status="error", error_message=str(e))
        raise
```

### Trace Context

The trace context maintains information about the current operation:

```python
class AgentTracer:
    def __init__(self, agent_name: str, logger: StructuredLogger):
        self.agent_name = agent_name
        self.logger = logger
        self.current_task = None
        self.start_time = None
    
    def start_task(self, task_name: str, **context):
        self.current_task = task_name
        self.start_time = time.time()
        self.logger.info({
            "agent": self.agent_name,
            "task": task_name,
            "event": "task_start",
            **context,
            "message": f"Agent {self.agent_name} started task: {task_name}"
        })
        
    def end_task(self, status: str, **context):
        if self.current_task and self.start_time:
            execution_time = time.time() - self.start_time
            self.logger.info({
                "agent": self.agent_name,
                "task": self.current_task,
                "event": "task_end",
                "status": status,
                "execution_time": execution_time,
                **context,
                "message": f"Agent {self.agent_name} completed task: {self.current_task}"
            })
            self.current_task = None
            self.start_time = None
```

## Performance Monitoring

Agent method execution times are monitored using decorators:

```python
def monitor_agent_method():
    """Decorator to monitor agent methods."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            agent_name = getattr(self, 'name', self.__class__.__name__)
            method_name = func.__name__
            
            # Log method start
            logger = logging.getLogger(f"{agent_name}.{method_name}")
            logger.info({
                "agent": agent_name,
                "method": method_name,
                "args": {f"arg_{i}_type": type(arg).__name__ for i, arg in enumerate(args)},
                "kwargs": kwargs,
                "message": f"Starting {agent_name}.{method_name}"
            })
            
            start_time = time.time()
            
            try:
                # Execute the method
                result = func(self, *args, **kwargs)
                
                # Calculate execution time
                execution_time = time.time() - start_time
                
                # Log successful completion
                logger.info({
                    "agent": agent_name,
                    "method": method_name,
                    "execution_time": execution_time,
                    "status": "success",
                    # Add summary of result depending on type
                    "result": summarize_result(result),
                    "message": f"Completed {agent_name}.{method_name}"
                })
                
                return result
                
            except Exception as e:
                # Log failure
                execution_time = time.time() - start_time
                logger.error({
                    "agent": agent_name,
                    "method": method_name,
                    "execution_time": execution_time,
                    "status": "error",
                    "error": str(e),
                    "message": f"Error in {agent_name}.{method_name}: {str(e)}"
                })
                raise
                
        return wrapper
    return decorator
```

## Citation Tracking

Citations are tracked throughout the system using the Citation Validator:

```python
def check_citations_in_analysis(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """Check if citations are present in analysis results."""
    stats = {
        "total_citable_items": 0,
        "items_with_citations": 0,
        "citation_sources": set()
    }
    
    # Check each citable item
    def _check_item(item):
        if isinstance(item, dict) and "content" in item:
            stats["total_citable_items"] += 1
            if "citation" in item and item["citation"]:
                stats["items_with_citations"] += 1
                if item["citation"] != "Internal Analysis":
                    stats["citation_sources"].add(item["citation"])
    
    # Process different sections of the analysis
    if "analysis" in analysis_results:
        # ... check each section ...
    
    # Calculate percentage
    stats["citation_percentage"] = (
        (stats["items_with_citations"] / stats["total_citable_items"] * 100) 
        if stats["total_citable_items"] > 0 else 0
    )
    
    logger.info(f"Citation stats: {stats['items_with_citations']}/{stats['total_citable_items']} items cited ({stats['citation_percentage']:.1f}%)")
    return stats
```

## Source Tracking

All data sources are tracked using the source validator:

```python
def log_source_summary(data: Dict[str, Any], prefix: str = "") -> None:
    """
    Log a summary of source information in the data structure.
    
    Args:
        data: The data to inspect
        prefix: Prefix for log messages
    """
    if isinstance(data, dict):
        # Check for _source field
        if "_source" in data:
            source_info = data["_source"]
            logger.info(f"{prefix}Source found: {source_info.get('name', 'Unknown')}")
```

## Error Handling

Errors are logged with context information to assist with troubleshooting:

```python
try:
    # API call implementation...
except requests.exceptions.RequestException as e:
    logger.error(f"Error fetching company profile for {ticker}: {str(e)}")
    return {"error": f"Failed to fetch company profile: {str(e)}"}
```

## LLM Call Logging

LLM API calls are logged with prompt information and token usage:

```python
def _call_llm(self, prompt: str):
    """Call LLM with prompt and return the raw text response."""
    
    # Log prompt length
    logger.debug(f"Calling LLM with prompt of length {len(prompt)}")
    
    # Make the API call
    response = self.standard_client.chat.completions.create(...)
    
    # Log token usage
    if hasattr(response, 'usage'):
        logger.debug(f"LLM call used {response.usage.prompt_tokens} prompt tokens, {response.usage.completion_tokens} completion tokens")
    
    return response.choices[0].message.content
```

## Custom Log Handlers

For production deployments, the system can be configured with custom handlers:

```python
# Example for JSON log format going to stdout
json_handler = logging.StreamHandler(sys.stdout)
json_handler.setFormatter(
    logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": %(message)s}')
)
logger.addHandler(json_handler)

# Example for file logging
file_handler = logging.FileHandler('financial_analysis.log')
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)
```

## Dashboard Integration

The system can export logs to monitoring systems:

```python
# Example for Prometheus metrics
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
llm_calls = Counter('llm_calls_total', 'Total number of LLM API calls', ['agent', 'method'])
llm_tokens = Counter('llm_tokens_total', 'Total number of tokens used', ['agent', 'direction'])
api_calls = Counter('api_calls_total', 'Total number of financial API calls', ['endpoint'])
execution_time = Histogram('execution_time_seconds', 'Method execution time', ['agent', 'method'])

# Start metrics endpoint
start_http_server(8000)

# Use in code
llm_calls.labels(agent='ResearchAgent', method='create_research_plan').inc()
```

## Visualization

For complex analyses, the observability data can be visualized:

```python
# Example for generating a trace visualization
def generate_trace_diagram(trace_data, output_file):
    """Generate a trace diagram from trace data."""
    import graphviz
    
    dot = graphviz.Digraph(comment='Execution Trace')
    
    # Add nodes and edges based on trace data
    for span in trace_data:
        dot.node(span['id'], f"{span['name']} ({span['duration_ms']}ms)")
        if span['parent_id']:
            dot.edge(span['parent_id'], span['id'])
    
    # Render to file
    dot.render(output_file, format='png')
```

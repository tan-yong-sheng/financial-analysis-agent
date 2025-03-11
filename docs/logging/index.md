# Logging and Observability

The Financial Analysis System uses structured logging for comprehensive observability across all components.

## Overview

The logging system provides:
- Structured JSON logs for machine-readable output
- Separate log streams for different components
- Performance metrics and timing data
- Request/response tracking for APIs
- Error tracking and diagnostics
- LLM interaction monitoring

## Documentation

- [Implementing Logging](implementing-logging.md) - Guide for adding logging to new components
- Log Analysis - Coming soon: Guide for analyzing and monitoring logs
- Metrics and Dashboards - Coming soon: Guide for setting up monitoring dashboards

## Log Types

### Agent Logs
Located in `logs/agents/`, these logs track:
- LLM interactions
- Agent decisions and operations
- Processing timelines
- Memory usage

### API Logs
Located in `logs/api/`, these logs track:
- External API calls
- Response times
- Rate limiting
- Data sizes
- Error rates

### Error Logs
Located in `logs/errors/`, these logs track:
- Exceptions and errors
- Stack traces
- Context data
- Recovery attempts

### General Logs
Located in `logs/general/`, these logs track:
- System operations
- Component initialization
- Configuration changes
- Overall metrics

## Log Format

All logs are in JSON format with standard fields:
```json
{
  "timestamp": "2025-03-11T04:20:00Z",
  "level": "INFO",
  "logger": "agent.planner",
  "message": "Process completed",
  "execution_time": 1.234,
  "method": "process",
  "additional_context": {
    "input_size": 1000,
    "output_size": 500
  }
}
```

## Key Features

1. **Structured Logging**
   - JSON format for machine processing
   - Consistent field names
   - Type-safe values

2. **Performance Tracking**
   - Method execution times
   - API latencies
   - Resource usage

3. **Error Handling**
   - Detailed error context
   - Stack traces
   - Recovery information

4. **Security**
   - Automatic PII redaction
   - API key protection
   - Sensitive data filtering

## Tools and Utilities

- `StructuredLogger`: Main logging class
- `monitor_agent_method`: Decorator for method monitoring
- `AgentTracer`: Agent activity tracking
- Log rotation and cleanup utilities

## Integration

The logging system integrates with:
- OpenAI API monitoring
- Financial data provider tracking
- Web research monitoring
- System health checks

## Configuration

Logging configuration is managed through:
- `config/logging.json` - Main configuration
- `config/logging_config.py` - Setup and initialization
- Environment variables for runtime settings

## Best Practices

1. Use structured logging for all components
2. Include relevant context in logs
3. Follow security guidelines for sensitive data
4. Monitor performance metrics
5. Implement proper error tracking
6. Maintain consistent log levels
7. Use appropriate log categories

## Further Reading

- [Testing Logging](../testing/writing-tests.md#testing-observability)
- [Contributing Guide](../contributing.md)
- [Architecture Overview](../architecture.md)

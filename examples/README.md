# Financial Analysis Agent Examples

This directory contains example scripts that demonstrate how to use different components of the Financial Analysis Agent system.

## Available Examples

1. **test_data_collection_agent.py** - Tests the DataCollectionAgent's ability to gather financial data
2. **test_analysis_agent.py** - Tests the AnalysisAgent's ability to analyze financial data
3. **test_orchestrator.py** - Tests the end-to-end orchestration of the financial analysis workflow
4. **test_individual_endpoints.py** - Tests individual API endpoints for troubleshooting

## How to Run the Examples

All examples can be run with a default ticker (AAPL) or with a ticker provided as a command line argument:

```bash
# Run with default ticker (AAPL)
python examples/test_data_collection_agent.py

# Run with specific ticker
python examples/test_data_collection_agent.py MSFT
```

## Troubleshooting

If you encounter issues:

1. Ensure your API keys are properly configured in the project's configuration
2. Check network connectivity to the API endpoints
3. Run the `test_individual_endpoints.py` script to verify specific API endpoints
4. Check the debug logs for detailed error information

## Adding New Examples

To add a new example:

1. Create a new Python file in the examples directory
2. Follow the pattern of existing examples
3. Add appropriate logging and error handling
4. Document your example in this README

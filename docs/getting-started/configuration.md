# Configuration Guide

This guide covers the configuration options for the Financial Analysis Agent system.

## Environment Variables

The system uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

```bash
# LLM API Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1  # Change if using a different provider
OPENAI_MODEL_NAME=gpt-4  # Or another compatible model
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=4000

# Financial Data API
FMP_API_KEY=your_financial_modeling_prep_api_key
FMP_BASE_URL=https://financialmodelingprep.com/api/v3

# Web Search API
SERPAPI_API_KEY=your_serpapi_api_key

# System Settings
LOG_LEVEL=INFO
AGENT_MEMORY_LIMIT=10
MAX_SEARCH_RESULTS=5
MAX_RESEARCH_DEPTH=3
DEFAULT_PERIOD=annual
DEFAULT_LIMIT=10
```

## Configuration Options

### LLM Settings

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_BASE_URL`: Base URL for the OpenAI API (or compatible provider)
- `OPENAI_MODEL_NAME`: Model to use (e.g., gpt-4, gpt-3.5-turbo)
- `OPENAI_TEMPERATURE`: Temperature setting (0.0-1.0)
- `OPENAI_MAX_TOKENS`: Maximum tokens to generate

### Financial Data Settings

- `FMP_API_KEY`: Financial Modeling Prep API key
- `FMP_BASE_URL`: Base URL for the FMP API
- `DEFAULT_PERIOD`: Default period for financial statements (annual or quarterly)
- `DEFAULT_LIMIT`: Default number of periods to retrieve

### Research Settings

- `SERPAPI_API_KEY`: SerpAPI key for web searches
- `MAX_SEARCH_RESULTS`: Maximum number of search results to process
- `MAX_RESEARCH_DEPTH`: Maximum depth for research (higher = more thorough)

### System Settings

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `AGENT_MEMORY_LIMIT`: Maximum items in agent memory

## Technical Indicators

The default technical indicators are configured in `config.py`:

```python
TECHNICAL_INDICATORS = ["sma", "ema", "rsi", "macd", "bollinger"]
```

To modify these, create a custom configuration file or edit the constants in `config.py`.

## Advanced Configuration

### Custom Models

To use alternative LLM providers:

1. Set `OPENAI_BASE_URL` to your provider's endpoint
2. Ensure the provider has an OpenAI-compatible API
3. Set `OPENAI_MODEL_NAME` to a model supported by your provider

Example for Azure OpenAI:

```bash
OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment
OPENAI_API_KEY=your_azure_openai_api_key
OPENAI_MODEL_NAME=your-deployment-name
```

### Logging Configuration

For advanced logging configuration, create a `logging.json` file:

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "simple": {
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "json": {
      "format": "%(json)s"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "simple",
      "stream": "ext://sys.stdout"
    },
    "file": {
      "class": "logging.FileHandler",
      "level": "DEBUG",
      "formatter": "json",
      "filename": "financial_analysis.log"
    }
  },
  "loggers": {
    "": {
      "level": "INFO",
      "handlers": ["console", "file"],
      "propagate": true
    }
  }
}
```

Load this configuration with:

```python
import logging.config
import json

with open('logging.json', 'r') as f:
    logging_config = json.load(f)
    logging.config.dictConfig(logging_config)
```

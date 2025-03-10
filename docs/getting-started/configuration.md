# Configuration Guide

## Environment Variables

The system uses several environment variables for configuration. These should be set in your `.env` file:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
FMP_API_KEY=your_financial_modeling_prep_api_key_here
SERPER_API_KEY=your_serper_api_key_here

# OpenAI Configuration
OPENAI_MODEL=gpt-4-turbo
OPENAI_TEMPERATURE=0.2
OPENAI_MAX_TOKENS=1500

# Analysis Parameters
DEFAULT_PERIOD=quarter
DEFAULT_LIMIT=4
```

## Analysis Parameters

You can customize various analysis parameters in `config.py`:

### OpenAI Settings
- `OPENAI_MODEL`: The OpenAI model to use
- `OPENAI_TEMPERATURE`: Controls randomness in responses (0.0-1.0)
- `OPENAI_MAX_TOKENS`: Maximum tokens per response

### Data Collection
- `DEFAULT_PERIOD`: Default period for financial statements ("quarter" or "annual")
- `DEFAULT_LIMIT`: Number of periods to fetch
- `TECHNICAL_INDICATORS`: List of technical indicators to calculate

### Research Settings
- `MAX_SEARCH_RESULTS`: Maximum number of web search results
- `MAX_RESEARCH_DEPTH`: Depth of research analysis

### Output Settings
- `REPORTS_DIR`: Directory for generated reports and charts

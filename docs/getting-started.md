# Getting Started

This guide will help you set up and run the Financial Analysis System.

## Prerequisites

- Python 3.8+ installed
- API keys for:
  - OpenAI (or compatible LLM API)
  - Financial Modeling Prep
  - SerpAPI (for web search capabilities)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/financial-analysis.git
cd financial-analysis
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_openai_base_url_or_openai_default
OPENAI_MODEL_NAME=gpt-4

SERPAPI_API_KEY=your_serpapi_api_key
FMP_API_KEY=your_financial_modeling_prep_api_key
```

## Running Your First Analysis

To analyze a company, use the main script with the ticker symbol:

```bash
python main.py --ticker AAPL
```

This will:

1. Collect financial data for Apple Inc.
2. Research current market trends and news
3. Analyze the financial data
4. Generate a comprehensive financial analysis report
5. Save the report in the `./reports` directory as `AAPL_analysis.md`

## Example Output

After running the analysis, you'll see output like:

```
==================================================
Analysis for AAPL completed successfully!
Full report saved to: /workspaces/codespaces-blank/reports/AAPL_analysis.md
Results summary saved to: /workspaces/codespaces-blank/reports/AAPL_results.json
==================================================
```

The generated report will be in Markdown format, making it easy to convert to other formats or view directly on platforms like GitHub.

## Customization Options

### Output Directory

By default, reports are saved to the `./reports` directory. You can specify a different directory:

```bash
python main.py --ticker AAPL --output /path/to/custom/directory
```

### Advanced Configuration

You can modify the system behavior by editing configuration options in `config.py`:

- `DEFAULT_PERIOD`: Choose between "annual" or "quarter" for financial statements
- `DEFAULT_LIMIT`: Number of historical periods to retrieve
- `TECHNICAL_INDICATORS`: List of technical indicators to calculate
- `OPENAI_TEMPERATURE`: Controls randomness in LLM responses

## Troubleshooting

### API Key Issues

If you encounter errors related to API keys, ensure:

1. Your `.env` file contains all required API keys
2. The API keys are valid and have sufficient credits
3. For custom LLM endpoints, verify the base URL is accessible

### Missing Financial Data

If financial data is missing:

1. Verify the ticker symbol is correct
2. Check if your Financial Modeling Prep API key has access to the required endpoints
3. Some smaller companies may have limited financial data available

### Memory or Performance Issues

For performance issues:

1. Consider reducing `DEFAULT_LIMIT` to retrieve fewer historical periods
2. Limit technical indicators to only those you need
3. For large reports, increase your system's available memory

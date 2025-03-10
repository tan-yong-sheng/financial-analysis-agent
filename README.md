# Financial Analysis System

An AI-powered financial analysis tool that automates comprehensive stock research, statement analysis, and report generation.

## Overview

This system provides automated financial analysis by collecting data from financial APIs, analyzing financial statements, processing technical indicators, and generating comprehensive reports. It leverages LLM (Large Language Models) technology to provide qualitative insights alongside quantitative analysis.

## Features

- **Comprehensive Financial Analysis**
  - Income statement analysis (revenue growth, profit margins, etc.)
  - Balance sheet analysis (liquidity ratios, solvency metrics, etc.)
  - Cash flow statement analysis (operating cash, free cash flow, etc.)
  - Technical indicators analysis

- **AI-Powered Insights**
  - Market research integration
  - Trend identification
  - Investment recommendation generation

- **Report Generation**
  - Markdown formatted reports
  - JSON data export
  - Fact-checked content

## Installation

### Prerequisites

- Python 3.8+
- API keys for:
  - OpenAI (or compatible LLM API)
  - Financial Modeling Prep
  - SerpAPI (for web search capabilities)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/financial-analysis.git
cd financial-analysis
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```plaintext
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_openai_base_url_or_openai_default
OPENAI_MODEL_NAME=gpt-4

SERPAPI_API_KEY=your_serpapi_api_key
FMP_API_KEY=your_financial_modeling_prep_api_key
```

## Usage

Run a financial analysis for a company:

```bash
python main.py --ticker AAPL
```

Or use the simplified runner:

```bash
python run.py AAPL
```

The system will:
1. Create a research plan
2. Collect financial data
3. Perform market research
4. Analyze the data
5. Generate a comprehensive report
6. Validate facts and citations

## Project Structure

```
financial-analysis-system/
├── agents/                  # Specialized agent modules
├── tools/                   # Utility tools and helpers
├── modules/                 # Core functionality modules
├── reports/                 # Generated reports and charts
├── docs/                    # Documentation
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Documentation

Detailed documentation is available in the `docs/` directory. To view:

1. Install MkDocs:
```bash
pip install mkdocs mkdocs-material
```

2. Serve documentation locally:
```bash
mkdocs serve
```

3. Visit `http://127.0.0.1:8000` in your browser

## License

MIT License

# Financial Analysis Agent System

A role-based AI system for comprehensive financial analysis using multiple specialized agents.

## Features

- Role-based agent architecture for specialized tasks
- Integration with Financial Modeling Prep API for financial data
- Web research capabilities using Serper API
- Interactive candlestick charts using HTML Canvas
- Comprehensive financial analysis and report generation
- Fact-checking and citation validation

## Prerequisites

- Python 3.8+
- Financial Modeling Prep API key
- OpenAI API key
- Serper API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd financial-analysis-agent
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.env`:
```plaintext
OPENAI_API_KEY=your_openai_api_key
FMP_API_KEY=your_financial_modeling_prep_api_key
SERPER_API_KEY=your_serper_api_key
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
financial-analysis-agent/
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

# Installation Guide

## Prerequisites

Before installing the Financial Analysis Agent System, ensure you have:

- Python 3.8 or higher
- API keys for:
  - Financial Modeling Prep
  - OpenAI
  - Serper (for web research)
- Pip package manager

## Step-by-Step Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd financial-analysis-agent
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```plaintext
OPENAI_API_KEY=your_openai_api_key
FMP_API_KEY=your_financial_modeling_prep_api_key
SERPER_API_KEY=your_serper_api_key
```

4. Verify installation:
```bash
python run.py AAPL
```

## Configuration

See the [Configuration](configuration.md) guide for detailed settings information.

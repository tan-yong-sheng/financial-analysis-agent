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

# Installation

This guide covers the installation process for the Financial Analysis Agent system.

## Prerequisites

- Python 3.8+
- API keys for:
  - OpenAI (or compatible LLM API)
  - Financial Modeling Prep
  - SerpAPI (for web search capabilities)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/financial-analysis-agent.git
cd financial-analysis-agent
```

### 2. Create a Virtual Environment

```bash
# With venv (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or with conda
conda create -n financial-analysis python=3.10
conda activate financial-analysis
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

Create a `.env` file in the root directory with your API keys:

```plaintext
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_openai_base_url_or_openai_default
OPENAI_MODEL_NAME=gpt-4

SERPAPI_API_KEY=your_serpapi_api_key
FMP_API_KEY=your_financial_modeling_prep_api_key
```

## Docker Installation

You can also run the system using Docker:

```bash
# Build the Docker image
docker build -t financial-analysis-agent .

# Run the container
docker run -it --env-file .env financial-analysis-agent
```

## Verifying Installation

To verify your installation is working correctly:

```bash
# Run a simple test
python -m pytest tests/test_setup.py

# Try a basic analysis
python run.py --ticker AAPL --quick
```

## Troubleshooting

If you encounter issues:

1. **API Key Issues**: Ensure all API keys are set correctly in your `.env` file
2. **Dependency Conflicts**: Try using a fresh virtual environment
3. **Model Access**: Verify you have access to the specified OpenAI model

For additional help, refer to the [GitHub issues page](https://github.com/yourusername/financial-analysis-agent/issues) or check the [troubleshooting guide](troubleshooting.md).

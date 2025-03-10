import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FMP_API_KEY = os.getenv('FMP_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

# API Base URLs
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

# OpenAI Configuration
OPENAI_MODEL = os.getenv('OPENAI_MODEL_NAME', 'gpt-4')
OPENAI_TEMPERATURE = 0.2
OPENAI_MAX_TOKENS = 4000

# Directories
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")

# Agent Configuration
AGENT_MEMORY_LIMIT = 10  # Number of recent messages to keep in agent memory

# Research Configuration
MAX_SEARCH_RESULTS = 10
MAX_RESEARCH_DEPTH = 3

# Financial Data Configuration
DEFAULT_PERIOD = "annual"
DEFAULT_LIMIT = 5
TECHNICAL_INDICATORS = ["sma", "ema", "rsi", "macd"]

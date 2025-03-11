import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI/LLM configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
OPENAI_MODEL = os.getenv('OPENAI_MODEL_NAME', 'gpt-4')  # Changed from OPENAI_MODEL_NAME
OPENAI_TEMPERATURE = 0.2  # Controls randomness in responses
OPENAI_MAX_TOKENS = 4000  # Added missing config

# API Keys
FMP_API_KEY = os.getenv('FMP_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

# Analysis configuration
DEFAULT_PERIOD = "annual"  # or "quarter"
DEFAULT_LIMIT = 5  # Number of periods to analyze
TECHNICAL_INDICATORS = ["rsi", "sma", "ema"]

# API Base URLs
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

# Directories
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")

# Agent Configuration
AGENT_MEMORY_LIMIT = 10  # Number of recent messages to keep in agent memory

# Research Configuration
MAX_SEARCH_RESULTS = 10
MAX_RESEARCH_DEPTH = 3

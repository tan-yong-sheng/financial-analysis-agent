# API Reference

This API reference documents the key classes, methods, and interfaces in the Financial Analysis System. Use this reference to understand the available functionality and how to interact with different components of the system.

## Agent Classes

### BaseAgent

The foundation class for all agent implementations.

```python
class BaseAgent:
    def __init__(self, role: str, agent_name: str, base_url: str = None, model_name: str = None)
    def _call_llm(self, prompt: str, temperature: Optional[float] = None) -> str
    def process(self, input_data: Any) -> Any
    def reset_memory()
```

### PlannerAgent

```python
class PlannerAgent(BaseAgent):
    def __init__(self, base_url: str = None, model_name: str = None)
    def create_research_plan(self, ticker: str, company_info: Dict[str, Any]) -> Dict[str, Any]
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
```

### DataCollectionAgent

```python
class DataCollectionAgent(BaseAgent):
    def __init__(self, base_url: str = None, model_name: str = None)
    def determine_data_needs(self, ticker: str, research_plan: Dict[str, Any]) -> Dict[str, Any]
    def collect_company_data(self, ticker: str, data_plan: Dict[str, Any]) -> Dict[str, Any]
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
```

### ResearchAgent

```python
class ResearchAgent(BaseAgent):
    def __init__(self, base_url: str = None, model_name: str = None)
    def web_search(self, query: str, num_results: int = MAX_SEARCH_RESULTS) -> List[Dict[str, Any]]
    def research_company_news(self, ticker: str, company_name: str) -> List[Dict[str, Any]]
    def research_industry_trends(self, industry: str, sector: str) -> Dict[str, Any]
    def research_competitors(self, ticker: str, company_name: str, industry: str) -> Dict[str, Any]
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
```

### AnalysisAgent

```python
class AnalysisAgent(BaseAgent):
    def __init__(self, base_url: str = None, model_name: str = None)
    def analyze_financial_data(self, financial_data: Dict[str, Any], research_plan: Dict[str, Any]) -> Dict[str, Any]
    def integrate_market_research(self, analysis_results: Dict[str, Any], research_results: Dict[str, Any]) -> Dict[str, Any]
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
```

### WriterAgent

```python
class WriterAgent(BaseAgent):
    def __init__(self, base_url: str = None, model_name: str = None)
    def generate_report_structure(self, ticker: str, company_info: Dict[str, Any], research_plan: Dict[str, Any]) -> Dict[str, Any]
    def write_report_section(self, section_name: str, section_template: Dict[str, Any], analysis_data: Dict[str, Any]) -> str
    def compile_full_report(self, report_template: Dict[str, Any], section_contents: Dict[str, str]) -> str
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
```

### FactCheckAgent

```python
class FactCheckAgent(BaseAgent):
    def __init__(self, base_url: str = None, model_name: str = None)
    def validate_financial_data(self, financial_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]
    def check_citations(self, report_content: str, financial_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]
    def add_citations(self, report_content: str, financial_data_sources: Dict[str, str]) -> str
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]
```

## Module Classes

### FinancialAnalyzer

```python
class FinancialAnalyzer:
    def __init__()
    def analyze_income_statement(self, income_data: List[Dict[str, Any]]) -> Dict[str, Any]
    def analyze_balance_sheet(self, balance_data: List[Dict[str, Any]]) -> Dict[str, Any]
    def analyze_cash_flow(self, cash_flow_data: List[Dict[str, Any]]) -> Dict[str, Any]
    def analyze_technical_data(self, technical_data: Dict[str, Any]) -> Dict[str, Any]
    def comprehensive_analysis(self, financial_data: Dict[str, Any]) -> Dict[str, Any]
```

## Tool Classes

### FinancialDataProvider

```python
class FinancialDataProvider:
    def __init__()
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]
    def get_company_profile(self, ticker: str) -> List[Dict[str, Any]]
    def get_income_statement(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]
    def get_balance_sheet(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]
    def get_cash_flow(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]
    def get_key_metrics(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]
    def get_financial_ratios(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]
    def get_stock_price(self, ticker: str, timeseries: int = 365) -> Dict[str, Any]
    def get_analyst_estimates(self, ticker: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]
    def get_technical_indicators(self, ticker: str, indicator: str, time_period: int = 14) -> Dict[str, Any]
```

### WebResearchTool

```python
class WebResearchTool:
    def __init__()
    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]
    def search_news(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]
    def get_company_competitors(self, company: str, industry: str) -> List[Dict[str, Any]]
    def get_industry_trends(self, industry: str) -> List[Dict[str, Any]]
```

### DataTransformer

```python
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj) -> Any
    
def convert_numpy_types(obj: Any) -> Any
def clean_and_convert_numeric(df: pd.DataFrame) -> pd.DataFrame
def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]
def prepare_data_for_report(data: Dict[str, Any]) -> Dict[str, Any]
```

## System Class

### FinancialAnalysisOrchestrator

```python
class FinancialAnalysisOrchestrator:
    def __init__()
    def analyze_company(self, ticker: str) -> Dict[str, Any]
```

## Configuration

### Config Variables

```python
# API Keys
OPENAI_API_KEY: str  # OpenAI API key for LLM access
FMP_API_KEY: str     # Financial Modeling Prep API key
SERPAPI_API_KEY: str # SerpAPI key for web searches

# API Base URLs
FMP_BASE_URL: str    # Financial Modeling Prep base URL

# OpenAI Configuration
OPENAI_MODEL: str    # Model name to use (default: gpt-4)
OPENAI_TEMPERATURE: float  # Creativity level (default: 0.2)
OPENAI_MAX_TOKENS: int     # Maximum tokens in response

# Directories
REPORTS_DIR: str     # Path to store generated reports

# Agent Configuration
AGENT_MEMORY_LIMIT: int  # Number of messages in agent memory

# Research Configuration
MAX_SEARCH_RESULTS: int  # Maximum search results to return
MAX_RESEARCH_DEPTH: int  # Maximum research depth

# Financial Data Configuration
DEFAULT_PERIOD: str  # Default financial statement period
DEFAULT_LIMIT: int   # Default number of periods to retrieve
TECHNICAL_INDICATORS: List[str]  # Default technical indicators
```

## Command Line Interface

### Main Script

```bash
# Basic usage
python main.py --ticker AAPL

# With custom output directory
python main.py --ticker MSFT --output /path/to/custom/directory
```

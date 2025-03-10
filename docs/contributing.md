# Contributing Guide

This guide provides instructions for developers who want to contribute to the Financial Analysis System. Whether you're fixing bugs, adding new features, or improving documentation, your contributions are welcome!

## Project Structure

The Financial Analysis System follows a modular architecture with three main component types:

1. **Agents**: LLM-powered components that handle reasoning, decision-making, and natural language processing
2. **Modules**: Core computational components that process data without LLM interaction
3. **Tools**: Utility functions and external service integrations

```
financial-analysis/
├── agents/                 # LLM-powered agent implementations
│   ├── base_agent.py       # Base class for all agents
│   ├── planner_agent.py    # Planning and research plan creation
│   ├── data_collection_agent.py  # Financial data collection
│   ├── research_agent.py   # Web research functionality
│   ├── analysis_agent.py   # Financial analysis and insights
│   ├── writer_agent.py     # Report generation
│   └── fact_check_agent.py # Validation and fact-checking
│
├── modules/                # Core computational modules
│   ├── financial_analyzer.py  # Financial calculations and metrics
│   └── data_collector.py   # Data collection coordination
│
├── tools/                  # Utility functions and external interfaces
│   ├── data_transformer.py # Data type handling and conversion
│   ├── financial_data_provider.py  # Financial API integration
│   └── web_research.py     # Web search functionality
│
├── utils/                  # Helper utilities
│   └── search.py           # Search client implementation
│
├── docs/                   # Documentation
├── reports/                # Generated reports
├── tests/                  # Test suites
├── orchestrator.py         # Main workflow orchestration
├── main.py                 # Entry point script
├── config.py               # Configuration settings
└── requirements.txt        # Dependencies
```

## Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/financial-analysis.git
   cd financial-analysis
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with required API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_BASE_URL=your_openai_base_url
   OPENAI_MODEL_NAME=gpt-4
   
   SERPAPI_API_KEY=your_serpapi_api_key
   FMP_API_KEY=your_financial_modeling_prep_api_key
   ```

## Coding Standards

The project follows these coding standards:

1. **PEP 8** for Python style guidelines
2. **Type hints** for all function parameters and return values
3. **Docstrings** for all classes and functions (Google docstring format)
4. **Error handling** with specific exception types and meaningful error messages
5. **Logging** for significant events and potential issues

Example function with proper style:

```python
def analyze_data(data: List[Dict[str, Any]], metrics: List[str]) -> Dict[str, float]:
    """
    Analyze financial data using specified metrics.
    
    Args:
        data (List[Dict[str, Any]]): The financial data to analyze
        metrics (List[str]): Metrics to calculate
        
    Returns:
        Dict[str, float]: Calculated metrics
        
    Raises:
        ValueError: If data is empty or metrics list is empty
    """
    if not data:
        raise ValueError("Data cannot be empty")
    if not metrics:
        raise ValueError("At least one metric must be specified")
        
    result = {}
    # Implementation...
    return result
```

## Adding New Components

### Adding a New Agent

1. Create a new Python file in the `agents` directory
2. Import and inherit from `BaseAgent`
3. Implement the `process` method and any required helper methods
4. Add the agent to the orchestrator workflow if needed

Example:
```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    """A custom agent that does something specific."""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        role = "a specialist that performs a specific task"
        super().__init__(role, "Custom Agent", base_url=base_url, model_name=model_name)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results."""
        # Implementation...
        return {"result": "processed data"}
```

### Adding a New Tool

1. Create a new Python file in the `tools` directory
2. Implement a class or functions for the tool's functionality
3. Add clear docstrings and error handling
4. Import and use the tool in relevant agents or modules

## Testing

The project uses Python's `unittest` framework for testing:

1. Write tests in the `tests` directory
2. Run tests using:
   ```bash
   python -m unittest discover
   ```

Example test:
```python
import unittest
from modules.financial_analyzer import FinancialAnalyzer

class TestFinancialAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = FinancialAnalyzer()
        self.sample_data = [...]
        
    def test_income_statement_analysis(self):
        result = self.analyzer.analyze_income_statement(self.sample_data)
        self.assertIn('summary', result)
        self.assertIn('growth', result)
        self.assertEqual(result['summary']['latest_revenue'], 1000000)
```

## Documentation

The project uses MkDocs with the Material theme for documentation:

1. Write documentation in Markdown format in the `docs` directory
2. Build documentation with:
   ```bash
   mkdocs build
   ```
3. View documentation locally with:
   ```bash
   mkdocs serve
   ```

## Pull Request Process

1. Fork the repository and create a branch for your feature or fix
2. Implement your changes following the coding standards
3. Add tests for new functionality
4. Update documentation as needed
5. Ensure all tests pass and the code lints without errors
6. Submit a pull request with a clear description of the changes

## Feature Requests and Bug Reports

Use the GitHub Issues system to report bugs or suggest features:

- **Bug reports**: Include steps to reproduce, expected behavior, and actual behavior
- **Feature requests**: Describe the feature, its benefits, and possible implementation approaches

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

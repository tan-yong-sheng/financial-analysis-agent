# Testing Guide

This guide covers the testing approach used in the Financial Analysis Agent system, including unit testing, integration testing, and model validation.

## Testing Framework

The system uses pytest as its primary testing framework:

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/agents/test_data_collection_agent.py

# Run with coverage report
pytest --cov=agents tests/
```

## Test Directory Structure

The tests follow a structure mirroring the main codebase:

```
tests/
├── agents/                 # Tests for agent modules
│   ├── test_base_agent.py
│   ├── test_data_collection_agent.py
│   ├── test_research_agent.py
│   └── ...
├── models/                 # Tests for data models
│   ├── test_research_models.py
│   └── ...
├── tools/                  # Tests for tools and utilities
├── utils/                  # Tests for utility functions
└── test_orchestrator.py    # Tests for main orchestrator
```

## Unit Testing

### Agent Testing

Each agent has unit tests for its methods:

```python
def test_get_company_profile_success(self, mock_get):
    """Test successful company profile retrieval."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = [{
        "companyName": "Test Company",
        "sector": "Technology",
        "industry": "Software"
    }]
    mock_get.return_value = mock_response
    
    # Call the method
    result = self.agent.get_company_profile("TEST")
    
    # Assertions
    assert result["companyName"] == "Test Company"
    assert result["sector"] == "Technology"
    assert result["industry"] == "Software"
    
    # Verify API call
    mock_get.assert_called_once_with(f"{self.agent.base_url}/profile/TEST?apikey={self.agent.api_key}")
```

### Model Testing

Pydantic models have validation tests:

```python
def test_citable_item_model():
    """Test CitableItem model validation"""
    # Valid data
    data = {
        "content": "Test content",
        "citation": "Test Source, 2023"
    }
    item = CitableItem(**data)
    assert item.content == "Test content"
    assert item.citation == "Test Source, 2023"
    
    # Citation is optional
    item_no_citation = CitableItem(content="Just content")
    assert item_no_citation.content == "Just content"
    assert item_no_citation.citation is None
```

### Schema Testing

Tests for JSON schema cleaning:

```python
def test_clean_schema_for_llm():
    """Test schema cleaning for LLM compatibility."""
    schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "default": {}  # Problematic default
                }
            }
        },
        "default": {}  # Root default
    }
    
    cleaned = clean_schema_for_llm(schema)
    
    # Assert defaults are removed
    assert "default" not in cleaned
    assert "default" not in cleaned["properties"]["items"]["items"]
```

## Integration Testing

Integration tests verify agent interactions:

```python
def test_orchestrator_data_research_flow():
    """Test data collection and research flow."""
    # Setup
    orchestrator = FinancialAnalysisOrchestrator()
    orchestrator.data_collector = MagicMock()
    orchestrator.researcher = MagicMock()
    
    # Configure mocks
    orchestrator.data_collector.get_company_profile.return_value = {"companyName": "Test Co"}
    orchestrator.data_collector.process.return_value = {"income_statement": []}
    orchestrator.researcher.create_research_plan.return_value = {"key_areas": []}
    orchestrator.researcher.process.return_value = {"analysis": {}}
    
    # Execute
    orchestrator._get_initial_company_data("TEST")
    orchestrator._create_research_plan({"ticker": "TEST", "company_data": {}})
    orchestrator._collect_financial_data({"ticker": "TEST", "research_plan": {}})
    
    # Verify
    orchestrator.data_collector.get_company_profile.assert_called_with("TEST")
    orchestrator.data_collector.process.assert_called_once()
    orchestrator.researcher.create_research_plan.assert_called_once()
```

## LLM Testing

Testing LLM interactions using mocks:

```python
def test_analyze_research_findings(mock_research_agent):
    """Test analyze_research_findings with structured output"""
    agent, mock_call = mock_research_agent
    
    # Setup mock
    analysis = ResearchAnalysis(
        market_trends=[
            CitableItem(content="Trend 1", citation="Source 1"),
            CitableItem(content="Trend 2", citation="Source 2")
        ],
        competitive_position=[
            CitableItem(content="Strong position", citation="Source 3")
        ],
        # ...other fields...
    )
    mock_call.return_value = analysis
    
    # Execute
    result = agent.analyze_research_findings({}, {})
    
    # Assert
    assert "analysis" in result
    assert len(result["analysis"]["market_trends"]) == 2
    assert result["analysis"]["market_trends"][0].content == "Trend 1"
```

## Citation Testing

Testing citation tracking and validation:

```python
def test_citation_validation():
    """Test citation validation utility"""
    analysis_results = {
        "analysis": {
            "market_trends": [
                {"content": "Trend 1", "citation": "Source 1"},
                {"content": "Trend 2"}  # Missing citation
            ],
            "competitive_position": [
                {"content": "Position 1", "citation": "Source 2"}
            ]
        }
    }
    
    stats = check_citations_in_analysis(analysis_results)
    
    assert stats["total_citable_items"] == 3
    assert stats["items_with_citations"] == 2
    assert stats["citation_percentage"] == 66.66666666666666
    assert set(stats["citation_sources"]) == {"Source 1", "Source 2"}
```

## Data Flow Testing

Testing the end-to-end flow of data through the system:

```python
def test_source_preservation():
    """Test that sources are preserved throughout the pipeline"""
    # Setup test data with sources
    financial_data = {
        "income_statement": [
            {"revenue": 100, "_source": {"name": "Test API"}}
        ]
    }
    
    # Mock orchestrator
    orchestrator = FinancialAnalysisOrchestrator()
    
    # Extract sources
    sources = orchestrator._extract_sources(financial_data)
    
    # Assert
    assert "income_statement" in sources
    assert sources["income_statement"]["name"] == "Test API"
```

## Running Tests

Run tests with logging disabled for cleaner output:

```bash
# Basic test run
pytest

# With coverage report
pytest --cov=.

# With detailed output
pytest -v

# Filter tests
pytest tests/agents/test_research_agent.py::test_create_research_plan

# Skip slow tests
pytest -k "not slow"
```

## Continuous Integration

Tests run automatically on push to the main repository, using GitHub Actions:

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

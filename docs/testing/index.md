# Testing Framework

## Overview

The Financial Analysis System uses pytest as its primary testing framework, with comprehensive test coverage across all major components. The testing infrastructure is designed to ensure reliability and maintainability of the system.

## Test Structure

```text
tests/
├── agents/                     # Agent component tests
│   ├── test_data_collection_agent.py
│   ├── test_report_agent.py
│   └── test_research_agent.py
├── modules/                    # Core module tests
│   └── test_financial_analyzer.py
├── tools/                     # Utility tests
│   └── test_data_transformer.py
├── conftest.py               # Shared test fixtures
├── test_orchestrator.py      # Main orchestrator tests
└── test_orchestrator_file_ops.py
```

## Test Fixtures

Common test fixtures are defined in `conftest.py` and provide standardized test data:

- `sample_income_statement`: Mock income statement data
- `sample_balance_sheet`: Mock balance sheet data
- `sample_cash_flow`: Mock cash flow statement
- `sample_technical_data`: Mock technical indicators
- `sample_company_profile`: Mock company information
- `sample_financial_data`: Combined financial dataset
- `mock_llm_response`: Mock LLM API responses

## Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/modules/test_financial_analyzer.py

# Run with coverage report
python -m pytest --cov=.

# Run with detailed output
python -m pytest -v
```

## Setting Up Tests

Before running tests, make sure your environment is properly set up:

```bash
# Install the package in development mode
pip install -e .

# Run the tests
python -m pytest
```

This ensures that Python can properly find all modules and packages within the project.

## Test Categories

### Agent Tests
- Test API interactions
- Verify error handling
- Check data transformations
- Validate agent-specific logic

### Module Tests
- Test financial calculations
- Verify data analysis methods
- Check error handling
- Validate output formats

### Tool Tests
- Test data cleaning utilities
- Verify type conversions
- Check serialization methods
- Validate transformation logic

### Integration Tests
- Test component interactions
- Verify end-to-end workflows
- Check file operations
- Validate orchestration logic

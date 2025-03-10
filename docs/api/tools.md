# Tools API Reference

## ChartGenerator

```python
from tools.chart_generator import ChartGenerator

generator = ChartGenerator(output_dir='reports')
chart_path = generator.create_candlestick_chart(
    price_data=data,
    ticker="AAPL",
    title="Apple Stock Price"
)
```

## DataTransformer

```python
from tools.data_transformer import DataTransformer

transformer = DataTransformer()
clean_data = transformer.clean_financial_data(raw_data)
metrics = transformer.normalize_metrics(clean_data, ['revenue', 'netIncome'])
trends = transformer.extract_quarterly_trends(clean_data, ['revenue'])
```

## WebResearchTool

```python
from tools.web_research import WebResearchTool

research = WebResearchTool()
results = research.search_google("AAPL earnings report 2024")
news = research.search_news("Apple stock analysis")
```

[View full tools documentation →](../components/tools.md)

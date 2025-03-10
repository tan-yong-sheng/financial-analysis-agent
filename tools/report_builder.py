import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json
from tools.chart_generator import ChartGenerator

class ReportBuilder:
    """Tool for building and formatting financial reports and creating visualizations."""
    
    def __init__(self, output_dir='reports'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.chart_generator = ChartGenerator(output_dir)
            
    def create_revenue_chart(self, income_data, ticker):
        """Create revenue trend chart."""
        if not income_data or 'raw_data' not in income_data:
            return None
            
        df = pd.DataFrame(income_data['raw_data'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        if 'revenue' not in df.columns:
            return None
        
        # Create plotly figure
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['date'],
            y=df['revenue'],
            name='Revenue'
        ))
        
        if 'netIncome' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['netIncome'],
                name='Net Income',
                line=dict(color='red', width=2)
            ))
        
        fig.update_layout(
            title=f"{ticker} - Revenue and Net Income Trends",
            xaxis_title="Period",
            yaxis_title="Amount",
            template="plotly_white"
        )
        
        # Save the image
        output_path = os.path.join(self.output_dir, f"{ticker}_revenue_trend.html")
        fig.write_html(output_path)
        
        return output_path
        
    def create_price_chart(self, stock_data, ticker):
        """Create stock price chart with technical indicators."""
        # Create interactive HTML canvas chart
        interactive_chart_path = self.chart_generator.create_candlestick_chart(
            stock_data, ticker, title=f"{ticker} - Interactive Stock Chart"
        )
        
        # Also create static chart as backup using existing plotly implementation
        static_chart_path = self._create_static_price_chart(stock_data, ticker)
        
        return {
            "interactive": interactive_chart_path,
            "static": static_chart_path
        }
        
    def _create_static_price_chart(self, stock_data, ticker):
        """Create static backup chart using plotly."""
        if not stock_data or 'raw_data' not in stock_data:
            return None
            
        df = pd.DataFrame(stock_data['raw_data'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Create plotly figure
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.1, 
                           subplot_titles=(f'{ticker} - Price Chart', 'Volume'),
                           row_heights=[0.7, 0.3])
                           
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ), row=1, col=1)
        
        # Add moving averages if available
        if 'SMA_50' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['SMA_50'],
                name='50-day MA',
                line=dict(color='blue', width=1)
            ), row=1, col=1)
            
        if 'SMA_200' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['SMA_200'],
                name='200-day MA',
                line=dict(color='red', width=1)
            ), row=1, col=1)
            
        # Add volume
        fig.add_trace(go.Bar(
            x=df['date'],
            y=df['volume'],
            name='Volume',
            marker_color='rgba(0, 0, 128, 0.5)'
        ), row=2, col=1)
        
        fig.update_layout(
            title=f"{ticker} - Stock Price Analysis",
            xaxis_rangeslider_visible=False,
            template="plotly_white"
        )
        
        # Save the image
        output_path = os.path.join(self.output_dir, f"{ticker}_stock_chart.html")
        fig.write_html(output_path)
        
        return output_path
        
    def format_markdown_report(self, report_content, charts=None):
        """
        Format a report with embedded charts.
        
        Args:
            report_content (str): The markdown content of the report
            charts (dict): Dictionary with section names as keys and chart paths as values
            
        Returns:
            str: The formatted report with chart references
        """
        if not charts:
            return report_content
            
        # Replace chart placeholders with links to the charts
        formatted_report = report_content
        
        for section, chart_path in charts.items():
            if chart_path and os.path.exists(chart_path):
                chart_ref = f"\n\n![{section} Chart]({chart_path})\n\n"
                # Try to insert chart after the section header
                section_pattern = f"## {section}"
                if section_pattern in formatted_report:
                    parts = formatted_report.split(section_pattern, 1)
                    formatted_report = parts[0] + section_pattern + chart_ref + parts[1]
                else:
                    # Append at the end if section not found
                    formatted_report += f"\n\n### {section} Chart\n{chart_ref}"
        
        return formatted_report

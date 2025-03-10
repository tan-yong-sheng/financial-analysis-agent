import json
import os
from datetime import datetime

class ChartGenerator:
    """Tool for generating interactive financial charts using HTML Canvas."""
    
    def __init__(self, output_dir='reports'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def create_candlestick_chart(self, price_data, ticker, title=None, template="dark"):
        """
        Generate an interactive candlestick chart using HTML Canvas.
        
        Args:
            price_data (dict/DataFrame): OHLCV data
            ticker (str): Stock ticker symbol
            title (str, optional): Chart title
            template (str): Chart theme ("dark" or "light")
            
        Returns:
            str: Path to generated HTML file
        """
        # Process input data
        if isinstance(price_data, dict) and 'raw_data' in price_data:
            price_data = price_data['raw_data']
            
        # Convert data to desired format for JavaScript
        chart_data = {
            'dates': [],
            'open': [],
            'high': [],
            'low': [],
            'close': [],
            'volume': [],
        }
        
        for item in price_data:
            if isinstance(item.get('date'), str):
                chart_data['dates'].append(item['date'])
            else:
                chart_data['dates'].append(item['date'].strftime('%Y-%m-%d'))
            chart_data['open'].append(item['open'])
            chart_data['high'].append(item['high'])
            chart_data['low'].append(item['low'])
            chart_data['close'].append(item['close'])
            chart_data['volume'].append(item['volume'])
        
        # Set chart colors based on template
        colors = {
            'dark': {
                'bg': '#1a1a1a',
                'grid': '#2d2d2d',
                'text': '#e0e0e0',
                'up': '#26a69a',
                'down': '#ef5350',
                'volume': 'rgba(100, 100, 100, 0.3)'
            },
            'light': {
                'bg': '#ffffff',
                'grid': '#f0f0f0',
                'text': '#333333',
                'up': '#00897b',
                'down': '#e53935',
                'volume': 'rgba(200, 200, 200, 0.5)'
            }
        }[template]
        
        # Generate HTML with embedded chart
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title or f"{ticker} - Stock Chart"}</title>
            <style>
                body {{ 
                    margin: 0;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                    background-color: {colors['bg']};
                    color: {colors['text']};
                }}
                .chart-container {{
                    position: relative;
                    margin: 0 auto;
                }}
                .toolbar {{
                    margin-bottom: 10px;
                    text-align: center;
                }}
                button {{
                    padding: 5px 15px;
                    margin: 0 5px;
                    border: none;
                    border-radius: 3px;
                    background: #444;
                    color: #fff;
                    cursor: pointer;
                }}
                button:hover {{
                    background: #555;
                }}
                canvas {{
                    border: 1px solid {colors['grid']};
                }}
            </style>
        </head>
        <body>
            <div class="toolbar">
                <button onclick="setTimeframe('1M')">1M</button>
                <button onclick="setTimeframe('3M')">3M</button>
                <button onclick="setTimeframe('6M')">6M</button>
                <button onclick="setTimeframe('1Y')">1Y</button>
                <button onclick="setTimeframe('ALL')">ALL</button>
                <button onclick="toggleOverlay('volume')">Volume</button>
                <button onclick="toggleOverlay('ma20')">MA20</button>
                <button onclick="toggleOverlay('ma50')">MA50</button>
            </div>
            <div class="chart-container">
                <canvas id="chart"></canvas>
            </div>
            
            <script>
            const chartData = {json.dumps(chart_data)};
            const colors = {json.dumps(colors)};
            
            // Chart configuration
            const config = {{
                showVolume: true,
                showMA20: false,
                showMA50: false,
                minPrice: Math.min(...chartData.low),
                maxPrice: Math.max(...chartData.high),
                candleWidth: 8,
                padding: {{ top: 50, right: 50, bottom: 50, left: 60 }}
            }};
            
            // Setup canvas
            const canvas = document.getElementById('chart');
            const ctx = canvas.getContext('2d');
            
            // Set canvas size
            function resizeCanvas() {{
                canvas.width = canvas.parentElement.clientWidth;
                canvas.height = window.innerHeight * 0.7;
                drawChart();
            }}
            
            window.addEventListener('resize', resizeCanvas);
            resizeCanvas();
            
            // Drawing functions
            function drawCandle(x, open, high, low, close) {{
                const isUp = close >= open;
                ctx.strokeStyle = isUp ? colors.up : colors.down;
                ctx.fillStyle = isUp ? colors.up : colors.down;
                
                // Draw wick
                ctx.beginPath();
                ctx.moveTo(x, high);
                ctx.lineTo(x, low);
                ctx.stroke();
                
                // Draw body
                const bodyHeight = Math.max(1, Math.abs(close - open));
                const y = Math.min(close, open);
                ctx.fillRect(x - config.candleWidth/2, y, config.candleWidth, bodyHeight);
            }}
            
            function calculateMA(period) {{
                const closes = chartData.close;
                const mas = [];
                
                for (let i = 0; i < closes.length; i++) {{
                    if (i < period - 1) {{
                        mas.push(null);
                        continue;
                    }
                    
                    let sum = 0;
                    for (let j = 0; j < period; j++) {{
                        sum += closes[i - j];
                    }}
                    mas.push(sum / period);
                }}
                
                return mas;
            }}
            
            function drawMA(data, color) {{
                ctx.beginPath();
                ctx.strokeStyle = color;
                ctx.lineWidth = 1;
                
                let first = true;
                data.forEach((value, i) => {{
                    if (value === null) return;
                    
                    const x = config.padding.left + (i * config.candleWidth) + (config.candleWidth / 2);
                    const y = scaleY(value);
                    
                    if (first) {{
                        ctx.moveTo(x, y);
                        first = false;
                    }} else {{
                        ctx.lineTo(x, y);
                    }}
                }});
                
                ctx.stroke();
            }}
            
            function scaleY(price) {{
                const range = config.maxPrice - config.minPrice;
                const chartHeight = canvas.height - config.padding.top - config.padding.bottom;
                return canvas.height - config.padding.bottom - 
                       ((price - config.minPrice) / range * chartHeight);
            }}
            
            function drawChart() {{
                // Clear canvas
                ctx.fillStyle = colors.bg;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw grid
                ctx.strokeStyle = colors.grid;
                ctx.lineWidth = 1;
                
                // Price grid lines
                const priceStep = (config.maxPrice - config.minPrice) / 5;
                for (let i = 0; i <= 5; i++) {{
                    const price = config.minPrice + (i * priceStep);
                    const y = scaleY(price);
                    
                    ctx.beginPath();
                    ctx.moveTo(config.padding.left, y);
                    ctx.lineTo(canvas.width - config.padding.right, y);
                    ctx.stroke();
                    
                    // Price labels
                    ctx.fillStyle = colors.text;
                    ctx.textAlign = 'right';
                    ctx.fillText(price.toFixed(2), config.padding.left - 5, y + 4);
                }}
                
                // Draw candlesticks
                for (let i = 0; i < chartData.dates.length; i++) {{
                    const x = config.padding.left + (i * config.candleWidth) + (config.candleWidth / 2);
                    drawCandle(
                        x,
                        scaleY(chartData.open[i]),
                        scaleY(chartData.high[i]),
                        scaleY(chartData.low[i]),
                        scaleY(chartData.close[i])
                    );
                }}
                
                // Draw moving averages
                if (config.showMA20) {{
                    const ma20 = calculateMA(20);
                    drawMA(ma20, '#2196F3');
                }}
                
                if (config.showMA50) {{
                    const ma50 = calculateMA(50);
                    drawMA(ma50, '#FF9800');
                }}
                
                // Draw volume
                if (config.showVolume) {{
                    const maxVolume = Math.max(...chartData.volume);
                    const volumeHeight = canvas.height * 0.2;
                    
                    for (let i = 0; i < chartData.dates.length; i++) {{
                        const x = config.padding.left + (i * config.candleWidth);
                        const height = (chartData.volume[i] / maxVolume) * volumeHeight;
                        const y = canvas.height - config.padding.bottom - height;
                        
                        ctx.fillStyle = colors.volume;
                        ctx.fillRect(x, y, config.candleWidth - 1, height);
                    }}
                }}
            }}
            
            // Event handlers
            function setTimeframe(period) {{
                // Implement timeframe changes
                console.log(`Setting timeframe to ${period}`);
                drawChart();
            }}
            
            function toggleOverlay(type) {{
                switch(type) {{
                    case 'volume':
                        config.showVolume = !config.showVolume;
                        break;
                    case 'ma20':
                        config.showMA20 = !config.showMA20;
                        break;
                    case 'ma50':
                        config.showMA50 = !config.showMA50;
                        break;
                }}
                drawChart();
            }}
            
            // Initial draw
            drawChart();
            </script>
        </body>
        </html>
        """
        
        # Save to file
        output_path = os.path.join(self.output_dir, f"{ticker}_candlestick_interactive.html")
        with open(output_path, "w") as f:
            f.write(html_content)
            
        return output_path

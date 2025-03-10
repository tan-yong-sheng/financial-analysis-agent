import sys
import os
import json
from openai import OpenAI

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS

class AIInsightGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens = OPENAI_MAX_TOKENS
        
    def _create_analysis_prompt(self, company_data, analysis_results):
        """Create a prompt for OpenAI to analyze financial data."""
        company_profile = company_data.get('company_profile', [{}])[0] if 'company_profile' in company_data else {}
        company_name = company_profile.get('companyName', 'the company')
        sector = company_profile.get('sector', 'its sector')
        
        prompt = f"""
        You are a professional financial analyst with expertise in equity research. 
        Analyze the following financial data for {company_name}, a company in {sector}.
        
        # Financial Data Summary:
        """
        
        # Add income statement insights
        if 'income_analysis' in analysis_results and 'error' not in analysis_results['income_analysis']:
            income_trends = analysis_results['income_analysis'].get('trends', {})
            prompt += "\n## Income Statement Analysis:\n"
            for metric, data in income_trends.items():
                if isinstance(data, dict) and 'current_value' in data:
                    qoq = data.get('qoq_change', 'N/A')
                    yoy = data.get('yoy_change', 'N/A')
                    prompt += f"- {metric}: Current value: {data['current_value']:.2f}, QoQ change: {qoq:.2f}%, YoY change: {yoy if yoy == 'N/A' else f'{yoy:.2f}%'}\n"
        
        # Add balance sheet insights
        if 'balance_sheet_analysis' in analysis_results and 'error' not in analysis_results['balance_sheet_analysis']:
            bs_trends = analysis_results['balance_sheet_analysis'].get('trends', {})
            prompt += "\n## Balance Sheet Analysis:\n"
            for metric, data in bs_trends.items():
                if isinstance(data, dict) and 'current_value' in data:
                    prompt += f"- {metric}: Current value: {data['current_value']:.2f}\n"
        
        # Add stock price analysis
        if 'stock_analysis' in analysis_results and 'error' not in analysis_results['stock_analysis']:
            stock_data = analysis_results['stock_analysis']
            prompt += f"\n## Stock Performance:\n"
            prompt += f"- Current price: {stock_data.get('current_price', 'N/A')}\n"
            prompt += f"- One-month return: {stock_data.get('one_month_return', 'N/A'):.2f}%\n"
            prompt += f"- Support level: {stock_data.get('support_level', 'N/A')}\n"
            prompt += f"- Resistance level: {stock_data.get('resistance_level', 'N/A')}\n"
            
            if stock_data.get('price_vs_sma50') is not None:
                prompt += f"- Price vs 50-day moving average: {stock_data['price_vs_sma50']:.2f}%\n"
            if stock_data.get('price_vs_sma200') is not None:
                prompt += f"- Price vs 200-day moving average: {stock_data['price_vs_sma200']:.2f}%\n"
            
        prompt += """
        # Analysis Tasks:
        
        1. Short-Term Analysis:
           - Identify key earnings trends from the quarterly results
           - Highlight significant price movements or technical patterns
           - Assess current valuation metrics relative to recent history
        
        2. Long-Term Analysis:
           - Evaluate the company's competitive position and growth prospects
           - Assess financial stability and balance sheet strength
           - Identify potential long-term catalysts or risks
        
        3. Risk Assessment:
           - Identify key financial, operational, or market risks
           - Evaluate the impact of external factors on performance
        
        4. Conclusion:
           - Summarize the key insights from your analysis
           - Highlight the most important metrics for investors to monitor
        
        Format your response as a structured financial research report with clearly labeled sections.
        Focus on providing data-driven insights rather than general observations.
        """
        
        return prompt
    
    def generate_insights(self, company_data, analysis_results):
        """Generate insights from financial analysis using OpenAI."""
        try:
            prompt = self._create_analysis_prompt(company_data, analysis_results)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional financial analyst with expertise in equity research."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            insights = response.choices[0].message.content
            return {
                "success": True,
                "insights": insights
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def generate_investment_recommendation(self, company_data, analysis_results, insights):
        """Generate investment recommendation based on analysis and insights."""
        try:
            prompt = f"""
            Based on the financial analysis and insights provided, generate a concise investment recommendation for the company.
            
            Financial Insights:
            {insights[:1000]}... (insights truncated for brevity)
            
            Your recommendation should include:
            1. An investment stance (Buy, Hold, or Sell)
            2. A summary of key factors supporting your recommendation
            3. Key risks to your investment thesis
            4. A suggested price target or valuation range (if applicable)
            
            Format your response in a structured, professional manner suitable for investors.
            Keep the recommendation concise and focused on actionable insights.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional financial analyst with expertise in equity research."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=800
            )
            
            recommendation = response.choices[0].message.content
            return {
                "success": True,
                "recommendation": recommendation
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

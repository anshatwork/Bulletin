import json
import os
from datetime import datetime
from typing import List, Dict

from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

class StockAnalysisRAG:
    def __init__(self):
        """Initialize the analysis pipeline with Ollama."""
        self.llm = ChatOllama(model="mistral", temperature=1)  # Using Mistral model from Ollama
        
    def process_stock_data(self, stock_data: Dict) -> str:
        """Process and format stock financial data."""
        # First try to find Eternal in peer company list
        eternal_data = None
        peer_companies = stock_data.get('peerCompanyList', [])
        
        for company in peer_companies:
            if company.get('name') == 'Eternal':
                eternal_data = company
                break
        
        # If we found Eternal in peer companies, use that data, otherwise fall back to main data
        data_source = eternal_data if eternal_data else stock_data
        
        metrics = [
            f"Price to Book Value Ratio: {data_source.get('priceToBookValueRatio', 'N/A')}",
            f"Price to Earnings Ratio: {data_source.get('priceToEarningsValueRatio', 'N/A')}",
            f"Market Cap: ${data_source.get('marketCap', 'N/A')}M",
            f"Current Price: ${data_source.get('price', 'N/A')}",
            f"Percent Change: {data_source.get('percentChange', 'N/A')}%",
            f"Net Change: ${data_source.get('netChange', 'N/A')}",
            f"Return on Equity (5Y Avg): {data_source.get('returnOnAverageEquity5YearAverage', 'N/A')}%",
            f"Return on Equity (TTM): {data_source.get('returnOnAverageEquityTrailing12Month', 'N/A')}%",
            f"Debt to Equity: {data_source.get('ltDebtPerEquityMostRecentFiscalYear', 'N/A')}",
            f"Net Profit Margin (5Y Avg): {data_source.get('netProfitMargin5YearAverage', 'N/A')}%",
            f"Net Profit Margin (TTM): {data_source.get('netProfitMarginPercentTrailing12Month', 'N/A')}%"
        ]
        
        return "\n".join(metrics)

    def process_news_data(self, news_data: List[Dict]) -> str:
        """Process and format news data."""
        formatted_news = []
        for article in news_data:
            if isinstance(article, dict):
                date = article.get('date', '')
                title = article.get('title', '')
                intro = article.get('intro', '')
                formatted_article = f"Date: {date}\nTitle: {title}\nSummary: {intro}\n"
                formatted_news.append(formatted_article)
        return "\n\n".join(formatted_news)

    def generate_recommendation(self, stock_data: Dict, news_data: List[Dict]) -> str:
        """Generate investment recommendation."""
        # Process data
        financial_metrics = self.process_stock_data(stock_data)
        news_articles = self.process_news_data(news_data)
        
        # Create prompt template
        prompt = PromptTemplate.from_template("""
        Based on the following stock information and news, provide a detailed investment recommendation.
        Consider the financial metrics, recent news sentiment, and market trends.
        
        Financial Metrics:
        {financial_metrics}
        
        Recent News:
        {news_articles}
        
        Please analyze the data and provide:
        1. Key strengths and concerns
        2. Recent developments and their impact
        3. Clear buy/hold/sell recommendation with reasoning
        4. Risk factors to consider
        
        Investment Recommendation:
        """)
        
        # Generate recommendation
        context = {
            "financial_metrics": financial_metrics,
            "news_articles": news_articles
        }
        
        response = self.llm.invoke(prompt.format(**context))
        return response.content

def main():
    # Load stock data
    with open('stock_data.json', 'r') as f:
        stock_data = json.load(f)
    
    # Initialize analysis pipeline
    analyzer = StockAnalysisRAG()
    
    # Generate recommendation
    recommendation = analyzer.generate_recommendation(stock_data, stock_data.get("news", []))
    print("\nInvestment Recommendation:")
    print(recommendation)

if __name__ == "__main__":
    main() 

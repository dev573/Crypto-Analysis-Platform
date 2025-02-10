from newsapi import NewsApiClient
import streamlit as st
from datetime import datetime, timedelta

class NewsAggregator:
    def __init__(self):
        # Initialize with a demo API key - replace with actual key in production
        self.newsapi = NewsApiClient(api_key='YOUR_NEWS_API_KEY')
        
    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_crypto_news(self, query="cryptocurrency", days=3):
        """Fetch cryptocurrency related news"""
        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            news = self.newsapi.get_everything(
                q=query,
                from_param=from_date,
                language='en',
                sort_by='relevancy'
            )
            return news.get('articles', [])
        except Exception as e:
            st.error(f"Error fetching news: {e}")
            return []

    def format_news_card(self, article):
        """Format news article for display"""
        return f"""
        <div class="news-card">
            <h4>{article['title']}</h4>
            <p>{article['description']}</p>
            <small>{article['publishedAt'][:10]} | Source: {article['source']['name']}</small>
        </div>
        """

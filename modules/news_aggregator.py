from newsapi import NewsApiClient
import streamlit as st
from datetime import datetime, timedelta

class NewsAggregator:
    def __init__(self):
        try:
            self.newsapi = NewsApiClient(api_key=st.secrets["NEWS_API_KEY"])
        except Exception as e:
            st.warning("News API key not configured. Please add your News API key to access news features.")
            self.newsapi = None

    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_crypto_news(self, query="cryptocurrency", days=3):
        """Fetch cryptocurrency related news"""
        try:
            if self.newsapi is None:
                return []

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
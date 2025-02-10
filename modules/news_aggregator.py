from newsapi import NewsApiClient
import streamlit as st
from datetime import datetime, timedelta

class NewsAggregator:
    def __init__(self):
        self.newsapi = None
        self._initialize_api()

    def _initialize_api(self):
        """Initialize News API client with proper error handling"""
        try:
            if "NEWS_API_KEY" in st.secrets:
                api_key = st.secrets["NEWS_API_KEY"]
                if api_key and api_key.strip():
                    self.newsapi = NewsApiClient(api_key=api_key)
        except Exception as e:
            st.warning("News API initialization failed. Some features may be limited.")
            self.newsapi = None

    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_crypto_news(_self, query="cryptocurrency", days=3):  # Changed 'self' to '_self'
        """Fetch cryptocurrency related news"""
        if _self.newsapi is None:
            return []

        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            news = _self.newsapi.get_everything(
                q=query,
                from_param=from_date,
                language='en',
                sort_by='relevancy'
            )
            return news.get('articles', [])
        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")
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
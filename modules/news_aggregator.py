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
            api_key = st.secrets.get("NEWS_API_KEY")
            if api_key:
                self.newsapi = NewsApiClient(api_key=api_key.strip())
                return
            st.warning("News API key not found or invalid in secrets")
        except Exception as e:
            st.error(f"Failed to initialize News API: {str(e)}")
        self.newsapi = None

    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_crypto_news(_self, query="cryptocurrency OR bitcoin OR ethereum", days=3):  # Changed 'self' to '_self'
        """Fetch cryptocurrency related news"""
        if _self.newsapi is None:
            return []

        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            news = _self.newsapi.get_everything(
                q=query,
                from_param=from_date,
                language='en',
                sort_by='relevancy',
                page_size=10
            )

            articles = news.get('articles', [])
            if not articles:
                st.info("No news articles found for the given criteria.")
                return []

            # Validate article data
            valid_articles = []
            for article in articles:
                if article.get('title') and article.get('description'):
                    valid_articles.append(article)

            return valid_articles

        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")
            return []

    def format_news_card(self, article):
        """Format news article for display"""
        try:
            return f"""
            <div class="news-card">
                <h4>{article.get('title', 'No Title')}</h4>
                <p>{article.get('description', 'No description available')}</p>
                <small>{article.get('publishedAt', '')[:10]} | Source: {article.get('source', {}).get('name', 'Unknown')}</small>
            </div>
            """
        except Exception as e:
            st.error(f"Error formatting news card: {str(e)}")
            return ""

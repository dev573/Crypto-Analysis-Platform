import streamlit as st
from textblob import TextBlob
import pandas as pd

class SentimentAnalyzer:
    @staticmethod
    def analyze_text(text):
        """Analyze sentiment of text using TextBlob"""
        if not text or not isinstance(text, str):
            return {'polarity': 0, 'subjectivity': 0}
        try:
            analysis = TextBlob(text)
            return {
                'polarity': analysis.sentiment.polarity,
                'subjectivity': analysis.sentiment.subjectivity
            }
        except Exception as e:
            st.error(f"Error analyzing sentiment: {e}")
            return {'polarity': 0, 'subjectivity': 0}

    @st.cache_data(ttl=900)
    def analyze_news_sentiment(_self, news_articles):  # Changed 'self' to '_self'
        """Analyze sentiment of news articles"""
        if not news_articles or not isinstance(news_articles, list):
            return pd.DataFrame({'sentiment': ['Neutral']})  # Return default dataframe

        sentiments = []
        for article in news_articles:
            try:
                title = article.get('title', '')
                description = article.get('description', '')

                if not title and not description:
                    continue

                title_sentiment = _self.analyze_text(title)
                desc_sentiment = _self.analyze_text(description)

                avg_polarity = (title_sentiment['polarity'] + desc_sentiment['polarity']) / 2
                sentiments.append({
                    'title': title,
                    'sentiment_score': avg_polarity,
                    'sentiment': 'Positive' if avg_polarity > 0 else 'Negative' if avg_polarity < 0 else 'Neutral'
                })
            except Exception as e:
                st.error(f"Error processing article: {str(e)}")
                continue

        if not sentiments:
            return pd.DataFrame({'sentiment': ['Neutral']})

        return pd.DataFrame(sentiments)
import streamlit as st
from textblob import TextBlob
import pandas as pd

class SentimentAnalyzer:
    @staticmethod
    def analyze_text(text):
        """Analyze sentiment of text using TextBlob"""
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
    def analyze_news_sentiment(self, news_articles):
        """Analyze sentiment of news articles"""
        sentiments = []
        for article in news_articles:
            title_sentiment = self.analyze_text(article['title'])
            desc_sentiment = self.analyze_text(article['description'])
            
            avg_polarity = (title_sentiment['polarity'] + desc_sentiment['polarity']) / 2
            sentiments.append({
                'title': article['title'],
                'sentiment_score': avg_polarity,
                'sentiment': 'Positive' if avg_polarity > 0 else 'Negative' if avg_polarity < 0 else 'Neutral'
            })
        return pd.DataFrame(sentiments)

import streamlit as st
import pandas as pd
from modules.crypto_data import CryptoDataProvider
from modules.news_aggregator import NewsAggregator
from modules.sentiment import SentimentAnalyzer
from utils.visualization import ChartCreator
from utils.cache import CacheManager
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Crypto Analysis Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize components
crypto_data = CryptoDataProvider()
news_aggregator = NewsAggregator()
sentiment_analyzer = SentimentAnalyzer()
chart_creator = ChartCreator()

# Sidebar
st.sidebar.title("⚙️ Settings")
time_range = st.sidebar.selectbox(
    "Time Range",
    ["24h", "7d", "30d", "90d"],
    index=1
)

# Main content
st.title("🚀 Crypto Analysis Platform")

# Top statistics
col1, col2, col3 = st.columns(3)

# Fetch top 50 cryptocurrencies
top_coins = crypto_data.get_top_50_coins()

with col1:
    st.metric(
        "Total Market Cap",
        f"${top_coins['market_cap'].sum():,.0f}",
        f"{top_coins['price_change_percentage_24h'].mean():.2f}%"
    )

with col2:
    st.metric(
        "24h Volume",
        f"${top_coins['total_volume'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Bitcoin Dominance",
        f"{(top_coins.iloc[0]['market_cap'] / top_coins['market_cap'].sum() * 100):.2f}%"
    )

# Market Overview
st.subheader("📊 Market Overview")
market_chart = chart_creator.create_market_overview(top_coins)
st.plotly_chart(market_chart, use_container_width=True)

# Top Cryptocurrencies
st.subheader("💎 Top Cryptocurrencies")
for idx, coin in top_coins.head(10).iterrows():
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.write(f"**{coin['name']} ({coin['symbol'].upper()})**")
    
    with col2:
        st.write(f"${coin['current_price']:,.2f}")
    
    with col3:
        change_color = "positive-change" if coin['price_change_percentage_24h'] > 0 else "negative-change"
        st.markdown(f"<span class='{change_color}'>{coin['price_change_percentage_24h']:.2f}%</span>", unsafe_allow_html=True)
    
    with col4:
        st.write(f"${coin['market_cap']:,.0f}")

# News and Sentiment
st.subheader("📰 Latest News & Sentiment")
news_articles = news_aggregator.get_crypto_news()
sentiment_df = sentiment_analyzer.analyze_news_sentiment(news_articles)

col1, col2 = st.columns([2, 1])

with col1:
    for article in news_articles[:5]:
        st.markdown(news_aggregator.format_news_card(article), unsafe_allow_html=True)

with col2:
    sentiment_fig = px.pie(
        sentiment_df,
        names='sentiment',
        title='News Sentiment Distribution',
        color_discrete_map={
            'Positive': '#43A047',
            'Neutral': '#FFA000',
            'Negative': '#FF6B6B'
        }
    )
    st.plotly_chart(sentiment_fig)

# Footer
st.markdown("---")
st.markdown("Data provided by CoinGecko API • Updated every 15 minutes")

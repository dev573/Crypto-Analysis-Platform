import streamlit as st
import pandas as pd
from modules.crypto_data import CryptoDataProvider
from modules.news_aggregator import NewsAggregator
from modules.sentiment import SentimentAnalyzer
from modules.price_predictor import PricePredictor # Added import
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
price_predictor = PricePredictor() # Added initialization
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

# News and Sentiment Analysis
st.subheader("📰 Latest News & Sentiment")

news_articles = news_aggregator.get_crypto_news()
if news_articles:
    try:
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
    except Exception as e:
        st.warning("Error processing news data. Some features may be limited.")
else:
    st.info("""
    ℹ️ News feature is currently disabled

    To enable cryptocurrency news and sentiment analysis:
    1. Get a free API key from newsapi.org
    2. Add it to .streamlit/secrets.toml file
    3. Restart the application

    Meanwhile, you can still use all other features of the platform!
    """)

# Top Cryptocurrencies with Predictions
st.subheader("💎 Top Cryptocurrencies")
st.markdown("""
<div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; font-weight: bold;">
    <div style="width: 30%">Coin</div>
    <div style="width: 15%">Price</div>
    <div style="width: 15%">24h Change</div>
    <div style="width: 20%">Market Cap</div>
    <div style="width: 20%">Prediction</div>
</div>
""", unsafe_allow_html=True)

for idx, coin in top_coins.head(10).iterrows():
    # Get prediction for each coin
    prediction = price_predictor.predict_price_movement(coin, sentiment_df) # Use the price predictor

    pred_color = price_predictor.get_prediction_color(prediction['prediction']) # Get color from predictor
    change_color = "positive-change" if coin['price_change_percentage_24h'] > 0 else "negative-change"

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; align-items: center;">
        <div style="width: 30%"><b>{coin['name']}</b> ({coin['symbol'].upper()})</div>
        <div style="width: 15%">${coin['current_price']:,.2f}</div>
        <div style="width: 15%" class="{change_color}">{coin['price_change_percentage_24h']:.2f}%</div>
        <div style="width: 20%">${coin['market_cap']:,.0f}</div>
        <div style="width: 20%">
            <span style="color: {pred_color}">
                {prediction['prediction']} ({prediction['confidence']:.1f}% confidence)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Data provided by CoinGecko API • News Sentiment Analysis • Updated every 15 minutes")
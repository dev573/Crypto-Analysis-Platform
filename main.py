import streamlit as st
import pandas as pd
from modules.crypto_data import CryptoDataProvider
from modules.news_aggregator import NewsAggregator
from modules.sentiment import SentimentAnalyzer
from modules.price_predictor import PricePredictor
from utils.visualization import ChartCreator
from utils.cache import CacheManager
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Crypto Analysis Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize components
crypto_data = CryptoDataProvider()
news_aggregator = NewsAggregator()
sentiment_analyzer = SentimentAnalyzer()
price_predictor = PricePredictor()
chart_creator = ChartCreator()

# Set time range to 24h
time_range = "24h"

# Main content
st.title("🚀 Crypto Analysis Platform")

# Top statistics
col1, col2, col3 = st.columns(3)

# Fetch initial data with 100 coins
top_coins = crypto_data.get_top_coins(limit=100)

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

# Initialize sentiment data
sentiment_df = pd.DataFrame()
news_articles = news_aggregator.get_crypto_news()
if news_articles:
    try:
        sentiment_df = sentiment_analyzer.analyze_news_sentiment(news_articles)
    except Exception as e:
        st.warning("Error processing news data. Some features may be limited.")

# Top Cryptocurrencies with Predictions
st.subheader("💎 Top Cryptocurrencies")

# Pagination controls
coins_per_page = st.select_slider(
    "Coins per page",
    options=[10, 20, 50],
    value=20
)

# Calculate pagination
total_pages = len(top_coins) // coins_per_page
current_page = st.select_slider(
    "Page",
    options=range(total_pages),
    value=0,
    format_func=lambda x: f"Page {x + 1} of {total_pages}"
)

# Calculate slice indices for current page
start_idx = current_page * coins_per_page
end_idx = start_idx + coins_per_page

st.markdown("""
<div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; font-weight: bold;">
    <div style="width: 20%">Coin</div>
    <div style="width: 12%">Price</div>
    <div style="width: 12%">24h Change</div>
    <div style="width: 12%">Predicted (24h)</div>
    <div style="width: 12%">Market Cap</div>
    <div style="width: 32%">Price Prediction & Factors</div>
</div>
""", unsafe_allow_html=True)

# Display coins for current page
for idx, coin in top_coins.iloc[start_idx:end_idx].iterrows():
    # Get prediction for each coin
    prediction = price_predictor.predict_price_movement(coin, sentiment_df)

    pred_color = price_predictor.get_prediction_color(prediction['prediction'])
    change_color = "positive-change" if coin['price_change_percentage_24h'] > 0 else "negative-change"

    # Calculate predicted price
    predicted_price = price_predictor.calculate_predicted_price(coin['current_price'], prediction)
    price_diff = ((predicted_price - coin['current_price']) / coin['current_price']) * 100
    pred_price_color = "positive-change" if price_diff > 0 else "negative-change"

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; align-items: center;">
        <div style="width: 20%"><b>{coin['name']}</b> ({coin['symbol'].upper()})</div>
        <div style="width: 12%">${coin['current_price']:,.2f}</div>
        <div style="width: 12%" class="{change_color}">{coin['price_change_percentage_24h']:.2f}%</div>
        <div style="width: 12%" class="{pred_price_color}">${predicted_price:,.2f}</div>
        <div style="width: 12%">${coin['market_cap']:,.0f}</div>
        <div style="width: 32%">
            <span style="color: {pred_color}">
                {prediction['prediction']} ({prediction['confidence']:.1f}% confidence)
            </span>
            <div style="font-size: 0.9em; margin-top: 4px; color: #666;">
                Sentiment: {prediction['sentiment_score']:.2f} • 
                Momentum: {prediction['price_momentum']:.1f}% • 
                Volume: {prediction['volume_indicator']:.2f}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# News and Sentiment Analysis
st.subheader("📰 Latest News & Sentiment")

if news_articles:
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
else:
    st.info("i️ News feature is currently disabled. Contact owner to enable.")

# Prediction Methodology Explanation
st.markdown("---")
st.subheader("📊 Understanding Our Price Predictions")

st.markdown("""
Our price prediction system combines three key factors to forecast cryptocurrency price movements:

1. **News Sentiment Score** (30% weight)
   - Range: -1.0 (Very Negative) to +1.0 (Very Positive)
   - Analyzes recent news articles' sentiment using natural language processing
   - Higher scores suggest positive market sentiment

2. **Price Momentum** (50% weight)
   - Based on 24-hour price changes
   - Indicates the strength and direction of recent price movements
   - Positive values suggest upward trend, negative values suggest downward trend

3. **Volume Indicator** (20% weight)
   - Ratio of trading volume to market cap
   - Measures market activity and liquidity
   - Higher values indicate stronger market interest

**Confidence Score Calculation:**
- Combines all three factors with their respective weights
- Higher confidence scores (closer to 100%) indicate stronger signals across multiple factors
- Lower confidence scores (closer to 50%) suggest mixed or weak signals

**Prediction Interpretation:**
- 🟢 **Up**: Combined factors suggest price increase
- 🔴 **Down**: Combined factors suggest price decrease
- 🟡 **Neutral**: Mixed signals or insufficient data

**Note**: These predictions are based on technical analysis and sentiment data. Always conduct your own research before making investment decisions.
""")

# Footer
st.markdown("---")
st.markdown("Data provided by CoinGecko API • News Sentiment Analysis • Updated every 15 minutes")

from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class CryptoDataProvider:
    def __init__(self):
        self.cg = CoinGeckoAPI()

    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_top_50_coins(_self):  # Changed 'self' to '_self' to make it hashable
        """Fetch top 50 cryptocurrencies by market cap"""
        try:
            coins = _self.cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=50,
                sparkline=True,
                price_change_percentage='24h,7d'
            )
            return pd.DataFrame(coins)
        except Exception as e:
            st.error(f"Error fetching cryptocurrency data: {e}")
            return pd.DataFrame()

    @st.cache_data(ttl=900)
    def get_coin_history(_self, coin_id, days=7):  # Changed 'self' to '_self'
        """Fetch historical data for a specific coin"""
        try:
            history = _self.cg.get_coin_market_chart_by_id(
                id=coin_id,
                vs_currency='usd',
                days=days
            )
            df = pd.DataFrame(history['prices'], columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            st.error(f"Error fetching historical data: {e}")
            return pd.DataFrame()

    def get_coin_details(self, coin_id):
        """Fetch detailed information for a specific coin"""
        try:
            return self.cg.get_coin_by_id(coin_id)
        except Exception as e:
            st.error(f"Error fetching coin details: {e}")
            return None
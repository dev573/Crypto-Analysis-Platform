import streamlit as st
from datetime import datetime, timedelta

class CacheManager:
    @staticmethod
    def get_cached_data(key, fetch_func, ttl_minutes=15):
        """Get cached data or fetch new data if cache expired"""
        cache_key = f"cache_{key}"
        timestamp_key = f"timestamp_{key}"
        
        cached_data = st.session_state.get(cache_key)
        cached_timestamp = st.session_state.get(timestamp_key)
        
        if cached_data is None or cached_timestamp is None or \
           datetime.now() - cached_timestamp > timedelta(minutes=ttl_minutes):
            data = fetch_func()
            st.session_state[cache_key] = data
            st.session_state[timestamp_key] = datetime.now()
            return data
        
        return cached_data

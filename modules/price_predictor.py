import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class PricePredictor:
    def __init__(self):
        self.sentiment_weights = {
            'Positive': 1,
            'Neutral': 0,
            'Negative': -1
        }

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def predict_price_movement(_self, coin_data, sentiment_data):
        """
        Predict price movement based on sentiment and recent price trends
        Returns: dict with prediction and confidence score
        """
        try:
            # Calculate sentiment score
            if not sentiment_data.empty and 'sentiment' in sentiment_data.columns:
                sentiment_scores = sentiment_data['sentiment'].map(_self.sentiment_weights)
                avg_sentiment = sentiment_scores.mean() if len(sentiment_scores) > 0 else 0
            else:
                avg_sentiment = 0

            # Calculate price momentum (last 24h trend)
            price_change_24h = coin_data.get('price_change_percentage_24h', 0)
            
            # Calculate volume trend
            volume_change = coin_data.get('total_volume', 0) / coin_data.get('market_cap', 1)
            
            # Combine factors with weights
            sentiment_weight = 0.3
            price_weight = 0.5
            volume_weight = 0.2
            
            combined_score = (
                avg_sentiment * sentiment_weight +
                (price_change_24h / 100) * price_weight +
                (volume_change - 0.5) * volume_weight
            )
            
            # Calculate prediction and confidence
            prediction = 'Up' if combined_score > 0 else 'Down'
            confidence = min(abs(combined_score) * 100, 100)
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'sentiment_score': avg_sentiment,
                'price_momentum': price_change_24h,
                'volume_indicator': volume_change
            }
            
        except Exception as e:
            st.error(f"Error in price prediction: {str(e)}")
            return {
                'prediction': 'Neutral',
                'confidence': 0,
                'sentiment_score': 0,
                'price_momentum': 0,
                'volume_indicator': 0
            }

    def calculate_predicted_price(self, current_price, prediction_data):
        """Calculate predicted price in 24 hours based on prediction data"""
        try:
            # Get the confidence and direction
            confidence = prediction_data['confidence'] / 100  # Convert to decimal
            is_up = prediction_data['prediction'] == 'Up'
            
            # Calculate potential change percentage based on confidence
            # Max change is set to 10% (can be adjusted based on volatility)
            max_change_percent = 10
            predicted_change = confidence * max_change_percent
            
            # Apply direction (positive or negative)
            if not is_up:
                predicted_change = -predicted_change
            
            # Calculate predicted price
            predicted_price = current_price * (1 + (predicted_change / 100))
            
            return predicted_price
        except Exception as e:
            st.error(f"Error calculating predicted price: {str(e)}")
            return current_price

    def get_prediction_color(self, prediction):
        """Return color based on prediction"""
        if prediction == 'Up':
            return '#43A047'
        elif prediction == 'Down':
            return '#FF6B6B'
        return '#FFA000'  # Neutral color

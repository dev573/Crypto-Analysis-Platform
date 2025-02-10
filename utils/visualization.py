import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

class ChartCreator:
    def __init__(self):
        self.chart_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FDCB6E']
        
    def create_price_chart(self, df, coin_name):
        """Create price chart for a cryptocurrency"""
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['price'],
                mode='lines',
                name=coin_name,
                line=dict(color='#1E88E5')
            )
        )
        
        fig.update_layout(
            title=f'{coin_name} Price History',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            template='plotly_white',
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        return fig

    def create_market_overview(self, df):
        """Create market overview visualization"""
        fig = px.treemap(
            df,
            path=[px.Constant("Cryptocurrencies"), 'name'],
            values='market_cap',
            color='price_change_percentage_24h',
            color_continuous_scale=['#FF6B6B', '#FFFFFF', '#43A047'],
            hover_data=['current_price', 'price_change_percentage_24h']
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=400
        )
        return fig

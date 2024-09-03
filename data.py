import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import streamlit as st 
from streamlit_navigation_bar import st_navbar
import yfinance as yf
import datetime as dt 
import plotly.graph_objs as go 

yf.pdr_override()

# NavBar
page = st_navbar(["Home", "Sec Fillings", "Models"])

st.title("Bloomberg Terminal Clone")

ticker = st.text_input("Enter a stock ticker symbol: ")

if ticker:
    # Create two columns with adjusted width ratios
    col1, col2 = st.columns([4, 1])  # Adjust the width ratio as needed
    
    with col1:
        # Chart
        fig = go.Figure()
        df = yf.download(tickers=ticker, period='5y', interval='1d')
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))

        fig.update_layout(
            title= str(ticker)+' Live Share Price:',
            yaxis_title='Stock Price (USD per Shares)'
        )               

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=5, label="5D", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=5, label="5Y", step="year", stepmode="backward"),
                    dict(step="all", label="Max")
                ])
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Stock information table
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Data for the table
        data = {
            "Metric 1": ["Market Cap", "Revenue (ttm)", "Net Income (ttm)", "Shares Out", "EPS (ttm)", "PE Ratio", "Forward PE", "Dividend", "Ex-Dividend Date"],
            "Value 1": [
                f"{info.get('marketCap', 'N/A'):,}", 
                f"{info.get('totalRevenue', 'N/A'):,}", 
                f"{info.get('netIncomeToCommon', 'N/A'):,}", 
                f"{info.get('sharesOutstanding', 'N/A') / 1e9:.2f}B", 
                info.get('trailingEps', 'N/A'), 
                info.get('trailingPE', 'N/A'), 
                info.get('forwardPE', 'N/A'), 
                f"${info.get('dividendRate', 'N/A')} ({info.get('dividendYield', 'N/A') * 100:.2f}%)", 
                info.get('exDividendDate', 'N/A')
            ],
            "Metric 2": ["Volume", "Open", "Previous Close", "Day's Range", "52-Week Range", "Beta", "Analysts", "Price Target", "Earnings Date"],
            "Value 2": [
                f"{info.get('volume', 'N/A'):,}", 
                info.get('open', 'N/A'), 
                info.get('previousClose', 'N/A'), 
                f"{info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}", 
                f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}", 
                info.get('beta', 'N/A'), 
                info.get('recommendationKey', 'N/A').capitalize(), 
                info.get('targetMeanPrice', 'N/A'), 
                info.get('earningsDate', 'N/A')
            ]
        }

        # Convert to DataFrame for display
        df = pd.DataFrame(data)
        table_html = df.to_html(index=False, header=False)
        
        # Display the table
        st.markdown(table_html, unsafe_allow_html=True)

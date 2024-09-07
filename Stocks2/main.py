import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Function to calculate Simple Moving Average (SMA)
def calculate_sma(data, window):
    return data.rolling(window=window).mean()

# Webpage Layout
st.set_page_config(page_title="Stock Analysis App", page_icon=":chart_with_upwards_trend:", layout="wide")

# Title and Description
st.title("Stock Analysis Dashboard")
st.write("""
    Welcome to the Stock Analysis Dashboard. Enter a stock symbol to view stock data, moving averages, 
    and trend indicators. This tool helps you track the market trends and make informed decisions.
""")

# Sidebar input
st.sidebar.header("Stock Input")
selected_stock = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
start_date = st.sidebar.date_input("Start Date", datetime(2021, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.now())

# Fetch stock data
try:
    stock_data = yf.download(selected_stock, start=start_date, end=end_date)
except Exception as e:
    st.error(f"Error fetching data: {e}")
    stock_data = None

# Check if the stock data is valid
if stock_data is not None and not stock_data.empty:
    st.subheader(f"Stock Data for {selected_stock}")
    st.write(stock_data.tail())

    # Plot stock closing price
    st.subheader(f"Closing Price of {selected_stock}")
    stock_data['Close'].plot(figsize=(10, 4))
    plt.title(f"{selected_stock} Closing Price", fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.xticks(rotation=45)
    st.pyplot()

    # Simple Moving Averages
    stock_data['100SMA'] = calculate_sma(stock_data['Close'], 100)
    stock_data['200SMA'] = calculate_sma(stock_data['Close'], 200)

    st.subheader(f"{selected_stock} - 100 Day & 200 Day Simple Moving Average (SMA)")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(stock_data['Close'], label='Closing Price')
    ax.plot(stock_data['100SMA'], label='100-Day SMA', color='green', linestyle='--')
    ax.plot(stock_data['200SMA'], label='200-Day SMA', color='red', linestyle='--')
    ax.set_title(f'{selected_stock} - Moving Averages')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    # Display Bullish or Bearish Signal
    if stock_data['100SMA'].iloc[-1] > stock_data['200SMA'].iloc[-1]:
        st.success(f"{selected_stock} is currently **Bullish** based on SMA.")
    else:
        st.error(f"{selected_stock} is currently **Bearish** based on SMA.")
else:
    st.error("No data available for the selected stock. Please check the stock symbol or date range.")

# Footer
st.write("---")
st.write("Developed by Sourabh | [GitHub](https://github.com/sourabhdangwal)")


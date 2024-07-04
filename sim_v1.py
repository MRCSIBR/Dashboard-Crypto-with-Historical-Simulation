import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

# List of cryptocurrencies (including USDT)
CURRENCIES = ["BTC", "XRP", "ETH", "DOGE", "USDT"]

# Mapping of cryptocurrencies to their Yahoo Finance symbols
YAHOO_SYMBOLS = {
    "BTC": "BTC-USD",
    "XRP": "XRP-USD",
    "ETH": "ETH-USD",
    "DOGE": "DOGE-USD",
    "USDT": "USDT-USD"
}

def fetch_historical_data(symbols, start_date):
    """Fetch historical price data for given symbols from Yahoo Finance."""
    data = yf.download(symbols, start=start_date, end=datetime.now())
    return data['Close']

def main():
    st.title("Crypto Portfolio Dashboard with Historical Simulation")

    # User input for holdings and start date
    st.sidebar.header("Enter Your Holdings and Start Date")
    holdings = {}
    for currency in CURRENCIES:
        if currency == "USDT":
            holdings[currency] = st.sidebar.number_input(f"{currency} holdings:", min_value=0.0, value=0.0, step=1.0)
        else:
            holdings[currency] = st.sidebar.number_input(f"{currency} holdings:", min_value=0.0, value=0.0, step=0.000001)

    start_date = st.sidebar.date_input("Select start date:", value=datetime.now() - timedelta(days=365))

    # Fetch historical data
    historical_data = fetch_historical_data([YAHOO_SYMBOLS[currency] for currency in CURRENCIES], start_date)

    # Calculate daily portfolio value
    portfolio_value = pd.DataFrame(index=historical_data.index)
    for currency in CURRENCIES:
        portfolio_value[currency] = historical_data[YAHOO_SYMBOLS[currency]] * holdings[currency]
    portfolio_value['Total'] = portfolio_value.sum(axis=1)

    # Create line chart of portfolio value over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=portfolio_value.index, y=portfolio_value['Total'],
                             mode='lines', name='Total Portfolio Value'))

    fig.update_layout(
        title='Historical Portfolio Value',
        xaxis_title='Date',
        yaxis_title='Portfolio Value (USD)',
        height=600
    )

    # Display the chart
    st.plotly_chart(fig)

    # Display current portfolio summary
    st.header("Current Portfolio Summary")
    current_prices = historical_data.iloc[-1]
    summary_df = pd.DataFrame({
        'Currency': CURRENCIES,
        'Holdings': [holdings[currency] for currency in CURRENCIES],
        'Current Price': [current_prices[YAHOO_SYMBOLS[currency]] for currency in CURRENCIES],
        'Value': [holdings[currency] * current_prices[YAHOO_SYMBOLS[currency]] for currency in CURRENCIES]
    })
    summary_df['Percentage'] = summary_df['Value'] / summary_df['Value'].sum() * 100
    summary_df = summary_df.sort_values('Value', ascending=False).reset_index(drop=True)
    st.table(summary_df.style.format({
        'Holdings': '{:.6f}',
        'Current Price': '${:.2f}',
        'Value': '${:.2f}',
        'Percentage': '{:.2f}%'
    }))

    # Display portfolio statistics
    st.header("Portfolio Statistics")
    st.write(f"Starting Value: ${portfolio_value['Total'].iloc[0]:.2f}")
    st.write(f"Current Value: ${portfolio_value['Total'].iloc[-1]:.2f}")
    st.write(f"Total Return: {((portfolio_value['Total'].iloc[-1] / portfolio_value['Total'].iloc[0]) - 1) * 100:.2f}%")
    st.write(f"Highest Value: ${portfolio_value['Total'].max():.2f}")
    st.write(f"Lowest Value: ${portfolio_value['Total'].min():.2f}")

if __name__ == "__main__":
    main()
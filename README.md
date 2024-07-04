# Dashboard-Crypto-with-Historical-Simulation

# Crypto Portfolio Dashboard with Historical Simulation

## Overview

This Streamlit-based web application provides a comprehensive dashboard for tracking and analyzing a cryptocurrency portfolio. It allows users to input their cryptocurrency holdings, visualize the portfolio's historical performance, and view current portfolio statistics.

## Features

- **Multiple Cryptocurrency Support**: Track BTC, XRP, ETH, DOGE, and USDT.
- **Custom Holdings Input**: Enter the quantity of each cryptocurrency in your portfolio.
- **Historical Simulation**: View your portfolio's performance from a selected start date (default: January 1, 2021) to the present.
- **Interactive Chart**: Visualize your portfolio's total value over time with an interactive line chart.
- **Current Portfolio Summary**: See a breakdown of your current holdings, including current prices and percentages.
- **Portfolio Statistics**: View key statistics such as starting value, current value, total return, highest value, and lowest value.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/crypto-portfolio-dashboard.git
   cd crypto-portfolio-dashboard
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run crypto_dashboard.py
   ```

2. Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8501`).

3. Use the sidebar to input your cryptocurrency holdings and select a start date for the historical simulation.

4. The main page will display:
   - A chart showing your portfolio's historical value
   - A summary of your current portfolio
   - Key statistics about your portfolio's performance

## Data Source

This dashboard uses Yahoo Finance (via the `yfinance` library) to fetch historical cryptocurrency price data.

## Customization

You can easily modify the `CURRENCIES` and `YAHOO_SYMBOLS` lists in the script to add or remove cryptocurrencies from the dashboard.

## Limitations

- The accuracy of the simulation depends on the availability and accuracy of historical data from Yahoo Finance.
- The dashboard does not account for transaction fees, taxes, or other costs associated with cryptocurrency trading.

## Contributing

Contributions to improve the dashboard are welcome! Please feel free to submit issues or pull requests.

## License

This project is open-source and available under the MIT License.

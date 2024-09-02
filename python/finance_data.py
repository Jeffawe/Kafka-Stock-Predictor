import yfinance as yf
from datetime import datetime, timedelta
import json

def get_stock_data_json(tickers, num_days=2, start_date='2022-01-01'):
    """
    Fetches historical stock data for the specified tickers from Yahoo Finance 
    and returns it in JSON format.
    
    Args:
        tickers (list): A list of stock ticker symbols (e.g., ["AMZN", "AAPL"]).
        start_date (str): The start date for fetching historical data in 'YYYY-MM-DD' format.
    
    Returns:
        str: JSON-formatted string containing stock data for the given tickers.
    """
    
    # Calculate end_date based on num_days or use today's date
    if num_days:
        end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=num_days)).strftime('%Y-%m-%d')
    else:
        end_date = datetime.now().strftime('%Y-%m-%d')

    # Initialize a list to hold all data in dictionary format
    all_data = []

    # Loop through each ticker and get historical data
    for ticker in tickers:
        # Create ticker instance
        stock = yf.Ticker(ticker)
        
        # Download historical data
        hist = stock.history(start=start_date, end=end_date)
        
        # Loop through the historical data to convert it to a list of dictionaries
        for index, row in hist.iterrows():
            record = {
                "Date": index.strftime('%Y-%m-%d'),  # Convert date to string
                "Ticker": ticker,
                "Open": row["Open"],
                "High": row["High"],
                "Low": row["Low"],
                "Close": row["Close"],
                "Volume": row["Volume"],
                "Dividend": row["Dividends"],
                "Stock Split": row["Stock Splits"]
            }
            all_data.append(record)
    
    return all_data

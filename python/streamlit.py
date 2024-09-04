import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
from write_to_ml import train_pipeline

data = {
    'Open': [194.48, 195.00, 196.50, 197.00],
    'High': [195.52, 196.00, 197.50, 198.00],
    'Low': [192.37, 193.00, 194.50, 195.00],
    'Close': [193.43, 194.00, 195.50, 196.00],
    'Volume': [54822100, 55000000, 56000000, 57000000],
    'Ticker': ["AMZN", "AAPL", "MSFT", "GOOGL"]
}

# Mapping of full company names to their tickers
company_to_ticker = {
    'Apple': 'AAPL',
    'Google': "GOOGL",
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN'
}

df = pd.DataFrame(data)

def load_pipeline():
    pipeline = joblib.load('../stock_price_pipeline.pkl')
    return pipeline

# Streamlit app
st.title('Stock Price Predictor')

st.write("""
### Important Notice
This model is for testing purposes only. It is not intended for use in production environments or for making real-life predictions.
""")


st.write("""
### Predict the Closing Price of a Stock
Enter the values for the 'Company', 'Open', 'High', 'Low', and 'Volume' to predict the 'Close' price of the stock.
""")

# Input fields for user to enter stock data
# Dropdown menu for selecting a company
company = st.selectbox('Select Company', list(company_to_ticker.keys()))

# Convert the selected company name to its ticker symbol
ticker = company_to_ticker[company]

open_price = st.number_input('Open Price', min_value=0.0, value=194.48, step=0.01)
high_price = st.number_input('High Price', min_value=0.0, value=195.52, step=0.01)
low_price = st.number_input('Low Price', min_value=0.0, value=192.37, step=0.01)
volume = st.number_input('Volume', min_value=0, value=54822100, step=100000)

# Predict button
if st.button('Predict Closing Price'):
    # Check if the model exists
    if not os.path.exists('stock_price_pipeline.pkl'):
        st.write("Model not found. Training a new model...")
        pipeline = train_pipeline()
    else:
        st.write("Loading existing model...")
        pipeline = load_pipeline()
    
    # Prepare input data as a DataFrame
    input_data = pd.DataFrame([[ticker, open_price, high_price, low_price, volume]], columns=['Ticker', 'Open', 'High', 'Low', 'Volume'])
    
    try:
        prediction = pipeline.predict(input_data)
        st.write(f"### Predicted Closing Price: ${prediction[0]:.2f}")
    except ValueError as e:
        st.write(f"Didn't train using the companies data. Try again another time. In the meantime, we'll work on getting that data")

# Show actual data used for model training
if st.checkbox('Show training data'):
    st.write(df)

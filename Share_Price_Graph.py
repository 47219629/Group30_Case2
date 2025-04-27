#Share_Price_Graph.py
# This script downloads the last twelve months of stock data for QUB.AX from Yahoo Finance
# and plots the closing prices over time. It also formats the x-axis labels to show the date in a more readable format.

# Import necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Set the ticker symbol for the stock you want to analyze
ticker_symbol = "QUB.AX"  

# Calculate the start and end dates for the 12-month period
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

# Download the historical stock data using yfinance
stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

#convert the 'Close' column to numeric values
stock_data.columns = stock_data.columns.droplevel(1)
stock_data['Close'] = pd.to_numeric(stock_data['Close'], errors='coerce')

# Check if data was downloaded successfully
if not stock_data.empty:
    # Plot the closing prices over time
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data.index, stock_data['Close'], label=f"{ticker_symbol} Stock Price")
    plt.title(f"{ticker_symbol} LTM Stock Price (AUD)", fontsize=20, fontweight='bold', pad=10)
    plt.legend(fontsize=16)
    plt.xlim([stock_data.index.min(), stock_data.index.max()])
    plt.xticks(stock_data.index[::60], fontsize=16)  # Show every 60th date on the x-axis
    plt.yticks(fontsize=16)
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
else:
    print(f"Error: No data found for {ticker_symbol} within the specified period.")

#Save the figure
plt.savefig('qub-asx-price-Graph.png')

#Add Comparison Share Price Graph
asx_data = yf.download('^AXJO', start=start_date, end=end_date)
asx_data.columns = stock_data.columns.droplevel(1)
asx_data['Close'] = pd.to_numeric(stock_data['Close'], errors='coerce')

#Percentage Change
stock_data['Returns'] = stock_data['Close'].pct_change()
asx_data['Returns'] = asx_data['Close'].pct_change()

if not stock_data.empty:
    # Plot the closing prices over time
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data.index, stock_data['Returns'], label=f"{ticker_symbol} Stock Price")
    plt.plot(asx_data.index, asx_data['Returns'], label='ASX 200 Index', color='orange')
    plt.title(f"{ticker_symbol} LTM Stock Price Changes (%)", fontsize=20, fontweight='bold', pad=10)
    plt.legend(fontsize=16)
    plt.xlim([stock_data.index.min(), stock_data.index.max()])
    plt.xticks(stock_data.index[::60], fontsize=16)  # Show every 60th date on the x-axis
    plt.yticks(fontsize=16)
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
else:
    print(f"Error: No data found for {ticker_symbol} within the specified period.")

#Save the figure
plt.savefig('qubvsaxjo-price-Graph.png')


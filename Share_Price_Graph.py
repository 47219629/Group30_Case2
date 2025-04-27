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
asx_data = yf.download('^AXJO', start=start_date, end=end_date)

#convert the 'Close' column to numeric values
stock_data.columns = stock_data.columns.droplevel(1)
asx_data.columns = stock_data.columns.droplevel(1)
stock_data['Close'] = pd.to_numeric(stock_data['Close'], errors='coerce')
asx_data['Close'] = pd.to_numeric(stock_data['Close'], errors='coerce')

# Check if data was downloaded successfully
if not stock_data.empty and not asx_data.empty:
    # Plot the closing prices over time
    # Set x-axis to show dates
    stock_data.index = pd.to_datetime(stock_data.index)
    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(10, 6))
    #Plot stock closing price as a line
    ax1.plot(stock_data.index, stock_data['Close'], label=f"{ticker_symbol} Stock Price", color='blue')
    #Plot ASX index as a line
    ax2 = ax1.twinx()  # Create a second y-axis
    ax2.plot(asx_data.index, asx_data['Close'], label='ASX 200 Index', color='orange')
    # Set the title and labels
    plt.title(f"{ticker_symbol} LTM Stock Price (AUD)", fontsize=20, fontweight='bold', pad=10)
    ax1.legend(fontsize=16, loc='upper left')
    ax2.legend(fontsize=16, loc='upper right')
    plt.xlim([stock_data.index.min(), stock_data.index.max()])
    plt.xticks(stock_data.index[::60], fontsize=16)  # Show every 60th date on the x-axis
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
else:
    print(f"Error: No data found for {ticker_symbol} within the specified period.")

#Save the figure
plt.savefig('qub-asx-price-Graph.png')



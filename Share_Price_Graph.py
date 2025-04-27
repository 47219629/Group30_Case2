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
stock_ticker = "QUB.AX"  
index_ticker = "^AXJO"  # ASX 200 Index ticker symbol

# Calculate the start and end dates for the 12-month period
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

# Download the historical stock data using yfinance
stock_data = yf.download([stock_ticker,index_ticker], start=start_date, end=end_date)
close_prices = stock_data['Close']

# Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

color1 = 'tab:blue'
color2 = 'tab:orange'

# First axis for the stock
ax1.plot(close_prices.index, close_prices[stock_ticker], color=color1, label=stock_ticker)
ax1.set_ylabel(stock_ticker+' Share Price (AUD)', color='black',fontsize=12)
ax1.set_xlim(start_date, end_date)
ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.to_datetime(x, unit='D').strftime('%b %Y')))

# Second axis for the index
ax2 = ax1.twinx()
ax2.plot(close_prices.index, close_prices[index_ticker], color=color2, linestyle='--', label='ASX 200 (^AXJO)')
ax2.set_ylabel('ASX200 Index Price (AUD)', color='black',fontsize=12)

# Title and legend
plt.title(f"{stock_ticker} vs ASX 200 Index",fontsize=16)
fig.tight_layout()
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

#Save the figure
plt.savefig('qub-asx-price-Graph.png')

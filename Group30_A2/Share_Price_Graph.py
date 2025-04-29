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
Broker_data=pd.read_csv('Broker_Targets.csv')

# Ensure the 'Date' column is in datetime format
Broker_data['Date'] = pd.to_datetime(Broker_data['Date'])
# Inspect and clean the 'Target Price' column
print("Inspecting 'Target Price' column for non-numeric values:")
print(Broker_data[~Broker_data['Target Price'].apply(lambda x: str(x).replace('.', '', 1).isdigit())])

# Convert 'Target Price' to numeric, coercing errors to NaN
Broker_data['Target Price'] = pd.to_numeric(Broker_data['Target Price'], errors='coerce')

# Fill NaN values with a default value or drop them if necessary
Broker_data['Target Price'] = Broker_data['Target Price'].fillna(method='ffill')
#Create a new Data Frame

Broker_dates=pd.DataFrame({
    'Date': pd.date_range(start=start_date, end=end_date)  
})
merged_broker_data = pd.merge(Broker_dates, Broker_data, on='Date', how='left')
merged_broker_data['Target Price'] = merged_broker_data['Target Price'].fillna(method='ffill')
if merged_broker_data['Target Price'].isnull().any():
    merged_broker_data['Target Price'].fillna(Broker_data['Target Price'].iloc[0], inplace=True)

# Plot
fig, ax1 = plt.subplots(figsize=(11, 6))

color1 = 'tab:blue'
color2 = 'tab:orange'

# First axis for the stock
ax1.plot(close_prices.index, close_prices[stock_ticker], color=color1, label=stock_ticker+' Share Price (LHS)')
# Plot the aligned Broker Target Price
ax1.plot(merged_broker_data['Date'], merged_broker_data['Target Price'], color='red', linestyle='--',label='Broker Target QUB Price (LHS)')
ax1.set_ylabel(stock_ticker+' Share Price (AUD)', color='black',fontsize=18)
ax1.set_xlim(start_date, end_date)
ax1.set_ylim(close_prices[stock_ticker].min()*0.95, close_prices[stock_ticker].max() * 1.05)  # Set y-axis limits
ax1.tick_params(axis='y', labelsize=14)
# Format the x-axis to show dates in "Mon YYYY" format
ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
# Second axis for the index
ax2 = ax1.twinx()
ax2.plot(close_prices.index, close_prices[index_ticker], color=color2, linestyle='--', label='ASX 200 (^AXJO) Index Price (RHS)')
ax2.set_ylabel('ASX200 Index Price (AUD)', color='black',fontsize=18)
ax2.set_ylim(close_prices[index_ticker].min()*0.95, close_prices[index_ticker].max() * 1.05)  # Set y-axis limits
ax2.tick_params(axis='y', labelsize=14)

# Title and legend
fig.tight_layout()
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=14, loc='upper left')

#Save the figure
plt.savefig('qub-asx-price-Graph.png')


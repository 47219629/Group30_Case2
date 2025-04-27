#Football_Field_Graph
#Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Import DCF file
DCF= pd.read_excel('QUB_DCF2.xlsx', 'Cover Page',usecols='F:I',nrows=6)
#Defining Variables
DCF = DCF.dropna()
Weighted_Price = DCF['Weighted_Price']
Target_Price = sum(Weighted_Price)

#Import Stock Data for Trading Range
import yfinance as yf
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

# Read DCF file cover page
Football_Field = pd.read_excel('QUB_DCF2.xlsx', 'Cover Page',usecols='A:D',nrows=5)
#Defining Variables
Football_Field = Football_Field.dropna()
Valuation_Method = Football_Field['Valuation_Method']
Valuation_Method = pd.concat([Valuation_Method, pd.Series(['12M Trading Range'])], ignore_index=True)
Min = Football_Field['Min']
Min = pd.concat([Min, pd.Series([min(stock_data['Close'])])], ignore_index=True)
Difference = Football_Field['Difference']
Difference = pd.concat([Difference, pd.Series([max(stock_data['Close']) - min(stock_data['Close'])])], ignore_index=True)
Max = Football_Field['Max']
Max = pd.concat([Max, pd.Series([max(stock_data['Close'])])], ignore_index=True)

#List for figure setup with max
Min_Dif=list(np.add(Min, Difference))
fig2, ax1 = plt.subplots(figsize=(13, 6))
#Set up horizontal bar chart
p1=plt.barh(Valuation_Method, Min, height=0.5, color='white')
p2=plt.barh(Valuation_Method, Difference, height=0.5,left=Min, color='#93B9DF')
p3=plt.barh(Valuation_Method, Max, height=0.5,left=Min_Dif, color='white')
plt.bar_label(p1, labels=[f'{bar.get_width():.2f}' for bar in p1], label_type='edge', fontsize=16, color='black', padding=-45)
plt.bar_label(p2, labels=[f'{bar.get_width():.2f}' for bar in p3], label_type='edge', fontsize=16, color='black', padding=10)
plt.axvline(x=float(stock_data['Close'].iloc[len(stock_data['Close'])-1].item()), color='r', linestyle='--', label='Spot Price: A${:.2f}'.format(stock_data['Close'].iloc[len(stock_data['Close'])-1].item()))
plt.legend(fontsize=12)  # Add legend to display the label
plt.axvline(x=float(Target_Price), color='g', linestyle='--', label='Target Price: A${:.2f}'.format(Target_Price))
plt.legend(fontsize=14,loc="upper left")  # Add legend to display the label
plt.title('Share Price (AUD) Using Different Valuation Methodologies', fontsize=20, fontweight='bold', pad=10, loc='center')
plt.tick_params(labelsize=16)
plt.xlim(1,6)

#Save Figure
plt.savefig('Football_Field.png', dpi=300, bbox_inches='tight')

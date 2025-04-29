import yfinance as yf
import numpy as np

def get_pe_ratio(last_price, earnings):
    return last_price / earnings

def get_eps(net_income, shares_outstanding):
    return net_income / shares_outstanding

def get_roa(net_income, total_assets):
    return (net_income / total_assets) *100

def get_current_ratio(current_assets, current_liabilities):
    return current_assets / current_liabilities

def get_debt_to_equity_ratio(total_liabilities, total_equity):
    return total_liabilities / total_equity

def get_quick_ratio(current_assets, current_liabilities, inventory):
    return (current_assets - inventory) / current_liabilities

def get_dividend_yield(dividend, last_price):
    return (dividend / last_price) *100

def round_2dp(ratios):
    """
    Rounds values of a tuple to 2 decimal places.
    """
    for key, value in ratios.items():
        # Checks if value is a number
        if isinstance(value, (int, float, np.floating)) and value is not None:
            rounded_value = round(float(value), 2)
            ratios[key] = rounded_value
        else:
            ratios[key] = value

    return ratios

def fetch_stock_data(TICKER):
    """
    Retrives relevant stock information based on a given stock ticker.
    """
    try:
        # Gets stock information
        tkr = yf.Ticker(TICKER)
        tkr_last_price = tkr.history(period="5y")
        tkr_info = tkr.info
        tkr_income_statement = tkr.financials
        tkr_balance_sheet = tkr.balance_sheet
        return tkr_last_price, tkr_info, tkr_income_statement, tkr_balance_sheet
    
    except Exception as e:
        print(f"Error: {e}")

def calc_ratios(tkr_last_price, tkr_info, tkr_income_statement, tkr_balance_sheet):
    """
    Calculates a tuple of ratios using stock information.
    """
    try:    
        # Extracts ratio related information
        dividend = tkr_info['lastDividendValue']
        shares_outstanding = tkr_info['sharesOutstanding']
        total_assets = (tkr_balance_sheet.loc["Total Assets"].iloc[0] + tkr_balance_sheet.loc["Total Assets"].iloc[1]) / 2
        last_price = tkr_last_price['Close'].iloc[-1]
        earnings = tkr_income_statement.loc["Net Income"].iloc[0]
        current_assets = tkr_balance_sheet.loc["Current Assets"].iloc[0]
        current_liabilities = tkr_balance_sheet.loc["Current Liabilities"].iloc[0]
        total_liabilities = tkr_balance_sheet.loc["Total Liabilities Net Minority Interest"].iloc[0]
        total_equity = tkr_balance_sheet.loc["Total Equity Gross Minority Interest"].iloc[0]
        inventory = tkr_balance_sheet.loc["Inventory"].iloc[0]

        # Calls relevant functions
        dividend_yield = get_dividend_yield(dividend, last_price)
        eps = get_eps(earnings, shares_outstanding)
        pe_ratio = get_pe_ratio(last_price, eps)
        roa = get_roa(earnings, total_assets)
        current_ratio = get_current_ratio(current_assets, current_liabilities)
        debt_to_equity_ratio = get_debt_to_equity_ratio(total_liabilities, total_equity)
        quick_ratio = get_quick_ratio(current_assets, current_liabilities, inventory)  

        ratios = {
            "Dividend Yield": dividend_yield,
            "EPS": eps,
            "P/E Ratio": pe_ratio,
            "ROA": roa,
            "Current Ratio": current_ratio,
            "Debt-to-Equity Ratio": debt_to_equity_ratio,
            "Quick Ratio": quick_ratio,
            }
        
        return round_2dp(ratios)
    
    except KeyError as e:
        print(f"KeyError: {e}")
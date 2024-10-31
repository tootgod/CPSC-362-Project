import pandas as pd
import csv
import SmaBacktest as sma
import DataManager as dm

def upper_lower(std_d, mid_line):
    for i in range(len(mid_line)):
        upper = mid_line[i] + (std_d[i] * 2)
        lower = mid_line[i] - (std_d[i] * 2)
    

def BB_backtest(historical_data, *, period=20, symbol, initial_balance=100000):
    dates = dm.getJsonDates(historical_data)
    closes = dm.getJsonCloses(historical_data)

    # Convert to pandas dataframe
    df = pd.DataFrame({
        'Date': pd.to_datetime(dates),
        'Close': closes
    })

    # Get middle line and standard deviations of each period
    df["MiddleLine"] = sma.calculate_sma(df['Close'], period)
    df["StdDeviation"] = df["MiddleLine"].rolling(window=period).std()
    
    
    # Backtest variables
    balance = initial_balance
    shares_held = 0
    trade_log = []
    
        

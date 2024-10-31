import pandas as pd
import csv
import SmaBacktest as sma
import DataManager as dm

def std_deviation(mean, date, period)
    
    return result

def BB_backtest(historical_data, *, period=20, symbol, initial_balance=100000):
    dates = dm.getJsonDates(historical_data)
    closes = dm.getJsonCloses(historical_data)

  
    df = pd.DataFrame({
        'Date': pd.to_datetime(dates),
        'Close': closes
    })
  
    df["MiddleLine"] = sma.calculate_sma(df['Close'], period)

    
  
    balance = initial_balance
    shares_held = 0
    trade_log = []

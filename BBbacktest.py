import pandas as pd
import csv
import SmaBacktest as sma
import DataManager as dm    

def BB_backtest(historical_data, period=20, symbol = 'BB', initial_balance=100000, std_dMult = 2):
    dates = dm.getJsonDates(historical_data)
    closes = dm.getJsonCloses(historical_data)

    # Convert to pandas dataframe
    df = pd.DataFrame({
        'Date': pd.to_datetime(dates),
        'Close': closes
    })

    # Get middle line and standard deviations of each period
    df['MiddleLine'] = sma.calculate_sma(df['Close'], period)
    df['StdDeviation'] = df['MiddleLine'].rolling(window=period).std()
    
    # Backtest variables
    balance = initial_balance
    shares_held = 0
    trade_log = []
    
    # Upper and lower bands of BB
    # Standard Deviation is multiplied by 2 by default
    for i in range(len(df)):
        upper.append(df['MiddleLine'].iloc[i] + (df['StdDeviation'].iloc[i] * std_dMult)
        lower.append(df['MiddleLine'].iloc[i] - (df['StdDeviation'].iloc[i] * std_dMult)

    df = pd.DataFrame({
        'UpperBand': upper,
        'LowerBand': lower
    })

    # Begin trading
    for i in range(len(df)):
        date = df['Date'].iloc[i]
        price = df['Close'].iloc[i]
        upper = df['UpperBand'].iloc[i]
        lower = df['LowerBand'].iloc[i]
        mid_line = df['MiddleLine'].iloc[i]
        
        '''add more signals and reactions to bollinger band actions'''
        '''such as: "narrow/narrowing bands", "wide/widening bands", "lower band bounce", "upper band bounce", etc''' 
        
        # Buy Signal (The middle line touches or goes under the lower band, indicating uptrend)
        if mid_line <= lower and shares_held == 0:
            shares_bought = balance // price
            transaction_amount = shares_bought * price
            balance -= transaction_amount
            shares_held = shares_bought
            sma.log_trade(trade_log, date, 'BUY', symbol, price, shares_bought, transaction_amount, balance)

        # Sell Signal (The middle line touches or goes over the upper band, indicating downtrend)
        elif mid_line >= upper and shares_held > 0:
            transaction_amount = shares_held * price
            gain_loss = transaction_amount - (shares_held * df['Close'].iloc[i])
            balance += transaction_amount
            sma.log_trade(trade_log, date, 'SELL', symbol, price, shares_held, transaction_amount, balance, gain_loss)
            shares_held = 0

    # Final sell
    final_price = df['Close'].iloc[-1]
    if shares_held > 0:
        transaction_amount = shares_held * final_price
        gain_loss = transaction_amount - (shares_held * df['Close'].iloc[-2])
        balance += transaction_amount
        log_trade(trade_log, df['Date'].iloc[-1], 'SELL (Final)', symbol, final_price, shares_held, transaction_amount, balance, gain_loss)
        shares_held = 0

    # Calculate final performance
    total_gain_loss = balance - initial_balance
    days = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days
    if days != 0:
        annual_return = ((1 + total_gain_loss / initial_balance) ** (365 / days) - 1) * 100
    else:
        annual_return = 0
    total_return = (balance - initial_balance) / initial_balance * 100

    # Add summary to log
    sma.log_summary(trade_log, total_gain_loss, annual_return, total_return, balance)

    # Save the log as CSV
    sma.save_trade_log(trade_log, f'{symbol}_trade_log.csv')

    return balance, total_gain_loss, annual_return, total_return

      

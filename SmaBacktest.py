# sma_backtest.py

import pandas as pd
import csv
import DataManager as dm

# SMA calculation function
def calculate_sma(data, window):
    return data.rolling(window=window).mean()

# Perform the SMA cross-over backtest
def backtest_sma(historical_data, short_window=50, long_window=200, initial_balance=100000, symbol="ETF"):
    dates = dm.getJsonDates(historical_data)
    closes = dm.getJsonCloses(historical_data)

    # Convert to pandas dataframe
    df = pd.DataFrame({
        'Date': pd.to_datetime(dates),
        'Close': closes
    })

    # Calculate SMAs
    df['SMA50'] = calculate_sma(df['Close'], short_window)
    df['SMA200'] = calculate_sma(df['Close'], long_window)

    # Backtest variables
    balance = initial_balance
    shares_held = 0
    trade_log = []

    # Backtest logic
    for i in range(1, len(df)):
        date = df['Date'].iloc[i]
        price = df['Close'].iloc[i]
        sma50 = df['SMA50'].iloc[i]
        sma200 = df['SMA200'].iloc[i]

        # Buy signal
        if df['SMA50'].iloc[i - 1] < df['SMA200'].iloc[i - 1] and sma50 > sma200 and shares_held == 0:
            shares_bought = balance // price
            transaction_amount = shares_bought * price
            balance -= transaction_amount
            shares_held = shares_bought
            log_trade(trade_log, date, 'BUY', symbol, price, shares_bought, transaction_amount, balance)

        # Sell signal
        elif df['SMA50'].iloc[i - 1] > df['SMA200'].iloc[i - 1] and sma50 < sma200 and shares_held > 0:
            transaction_amount = shares_held * price
            gain_loss = transaction_amount - (shares_held * df['Close'].iloc[i - 1])
            balance += transaction_amount
            log_trade(trade_log, date, 'SELL', symbol, price, shares_held, transaction_amount, balance, gain_loss)
            shares_held = 0

    # Final sell if shares are still held
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
    log_summary(trade_log, total_gain_loss, annual_return, total_return, balance)

    # Save the log as CSV
    save_trade_log(trade_log, f'{symbol}_trade_log.csv')

    return balance, total_gain_loss, annual_return, total_return

# Function to log each trade
def log_trade(trade_log, date, action, symbol, price, shares, transaction_amount, balance, gain_loss=None):
    trade_log.append({
        'Date': date.strftime('%Y-%m-%d'),
        'Action': action,
        'Symbol': symbol,
        'Price': price,
        'Shares': shares,
        'Transaction Amount': transaction_amount,
        '$Gain/Loss': gain_loss if gain_loss else 0,
        'Balance': balance,
        'Annual Return': '',
        'Total Return': ''
    })

# Function to log the summary
def log_summary(trade_log, total_gain_loss, annual_return, total_return, balance):
    trade_log.append({
        'Date': 'SUMMARY',
        'Action': '',
        'Symbol': '',
        'Price': '',
        'Shares': '',
        'Transaction Amount': '',
        '$Gain/Loss': total_gain_loss,
        'Balance': balance,
        'Annual Return': annual_return,
        'Total Return': total_return
    })

# Function to save the trade log as a CSV file
def save_trade_log(trade_log, filename):
    keys = trade_log[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(trade_log)
    print(f'Trade log saved to {filename}')

#driver code: comment out when running the main program
#backtest_sma(dm.loadData())
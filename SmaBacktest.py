# sma_backtest.py

from Backtest import Backtest
import pandas as pd  
from datetime import datetime
import csv


<<<<<<< HEAD
# Perform the SMA cross-over backtest
def backtest_sma(sec, short_window=25, long_window=75, initial_balance=100000, symbol="SMA"):
    dates = sec.historical_dates
    closes = sec.historical_closes

    # Convert to pandas DataFrame
    df = pd.DataFrame({
        'Date': pd.to_datetime(dates, unit='s'),# Convert Unix timestamps to datetime
        'DateUnix': dates,
        'Close': closes
    })
=======
class SMABacktest(Backtest):
    def calculate_sma(self, window):
        return self.closes.rolling(window=window).mean()

    def backtest(self, short_window=10, long_window=100):
        # Calculate SMAs
        short_sma = self.calculate_sma(short_window)
        long_sma = self.calculate_sma(long_window)
        
        for i in range(1, len(self.closes)):
            date = self.dates.iloc[i]
            price = self.closes.iloc[i]
>>>>>>> 9dd8bf2 (Added inheritance rules and fixed SMA)

            # Buy signal: short SMA crosses above long SMA
            if short_sma[i] > long_sma[i] and short_sma[i - 1] <= long_sma[i - 1] and self.position == 0:
                self.position = 1
                self.shares = self.balance // price
                transaction_amount = self.shares * price
                self.balance -= transaction_amount
                self.trades.append((date, 'Buy', self.symbol, price, self.shares, transaction_amount, 0, self.balance, self.total_return))
                print(f"Buying at {price} on {date}")

<<<<<<< HEAD
    # Initialize backtest variables
    balance = initial_balance
    shares_held = 0
    trade_log = []

    balanceList = [initial_balance]
    num = [0]
    

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
            balanceList.append(balanceList[-1] + (transaction_amount *-1))
            num.append(num[-1]+1)
            shares_held = shares_bought
            log_trade(trade_log, date, 'BUY', symbol, price, shares_bought, transaction_amount, balance)
            print(f"Logged BUY trade: {trade_log[-1]}")  # Debug print

        # Sell signal
        elif df['SMA50'].iloc[i - 1] > df['SMA200'].iloc[i - 1] and sma50 < sma200 and shares_held > 0:
            transaction_amount = shares_held * price
            gain_loss = transaction_amount - (shares_held * df['Close'].iloc[i - 1])
            balance += transaction_amount
            balanceList.append(balanceList[-1] + transaction_amount)
            num.append(num[-1]+1)
            log_trade(trade_log, date, 'SELL', symbol, price, shares_held, transaction_amount, balance, gain_loss)
            shares_held = 0
            print(f"Logged SELL trade: {trade_log[-1]}")  # Debug print

    # Final sell if shares are still held
    final_price = df['Close'].iloc[-1]
    if shares_held > 0:
        transaction_amount = shares_held * final_price
        gain_loss = transaction_amount - (shares_held * df['Close'].iloc[-2])
        balance += transaction_amount
        balanceList.append(balanceList[-1] + transaction_amount)
        num.append(num[-1]+1)
        log_trade(trade_log, df['Date'].iloc[-1], 'SELL (Final)', symbol, final_price, shares_held, transaction_amount, balance, gain_loss)
        shares_held = 0
        print(f"Logged final SELL trade: {trade_log[-1]}")  # Debug print

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
    print("Logged summary:", trade_log[-1])  # Debug print for summary

    # Print the entire trade_log before saving to check structure
    print("Final trade_log before saving:", trade_log)

    # Save the log as CSV
    save_trade_log(trade_log, f'{symbol}_trade_log.csv')

    return balance, total_gain_loss, annual_return, total_return, balanceList, num


# Function to log each trade
def log_trade(trade_log, date, action, symbol, price, shares, transaction_amount, balance, gain_loss=None):
    trade_log.append({
        'Date': date.strftime('%Y-%m-%d'),
        'Action': action or '',  # Replace None with an empty string
        'Symbol': symbol or '',  # Replace None with an empty string
        'Price': float(price) if price is not None else '',  # Convert to float or empty string
        'Shares': float(shares) if shares is not None else '',  # Convert to float or empty string
        'Transaction Amount': float(transaction_amount) if transaction_amount is not None else '',  # Convert to float or empty string
        '$Gain/Loss': float(gain_loss) if gain_loss is not None else 0,  # Use 0 if gain_loss is None
        'Balance': float(balance) if balance is not None else '',  # Convert to float or empty string
        'Annual Return': '',  # Leave empty for trade entries
        'Total Return': ''    # Leave empty for trade entries
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
        '$Gain/Loss': float(total_gain_loss) if total_gain_loss is not None else 0,
        'Balance': float(balance) if balance is not None else '',
        'Annual Return': float(annual_return) if annual_return is not None else '',
        'Total Return': float(total_return) if total_return is not None else ''
    })


# Function to save the trade log as a CSV file
def save_trade_log(trade_log, filename):
    print(f"Saving trade log to {filename}")
    if len(trade_log) <= 1:  # Only summary or empty log
        print(f"No trades recorded, skipping CSV save for {filename}.")
        return  # Exit if there are no trades to log

    # Ensuring all values are string-compatible for CSV output
    formatted_trade_log = []
    for entry in trade_log:
        formatted_entry = {}
        for key, value in entry.items():
            # Convert numpy floats and None values to appropriate types for CSV
            if isinstance(value, float):
                if key in ['Price', 'Shares', 'Transaction Amount', 'Balance']:
                    formatted_entry[key] = f"{value:,.2f}"  # Format with two decimal places
                elif key in ['$Gain/Loss', 'Annual Return', 'Total Return']:
                    formatted_entry[key] = f"{value:,.2f}" if value != 0 else ''  # Format, but skip 0 for $Gain/Loss in trades
                else:
                    formatted_entry[key] = str(value)  # Keep as is for strings
            elif isinstance(value, int):
                formatted_entry[key] = f"{value:,}"  # Use commas for large integers
            elif value is None:
                formatted_entry[key] = ''  # Use empty string for None values
            else:
                formatted_entry[key] = value  # Keep as is for strings
        formatted_trade_log.append(formatted_entry)

    # Insert a blank row before the summary for visual separation
    summary_row = None
    for i, entry in enumerate(formatted_trade_log):
        if entry['Date'] == 'SUMMARY':
            summary_row = formatted_trade_log.pop(i)
            break

    # Writing to CSV
    keys = formatted_trade_log[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(formatted_trade_log)

        # Add a blank line before the summary
        if summary_row:
            output_file.write('\n')
            dict_writer.writerow(summary_row)
        # Write the summary row separately
    print(f'Trade log saved to {filename}')
    print("Trade log save completed.")

    
=======
            # Sell signal: short SMA crosses below long SMA
            elif short_sma[i] < long_sma[i] and short_sma[i - 1] >= long_sma[i - 1] and self.position == 1:
                self.position = 0
                transaction_amount = self.shares * price
                gain_loss = transaction_amount - self.trades[-1][5]
                self.balance += transaction_amount
                self.total_return = ((self.balance - self.initial_balance) / self.initial_balance) * 100
                self.trades.append((date, 'Sell', self.symbol, price, self.shares, transaction_amount, gain_loss, self.balance, self.total_return))
                print(f"Selling at {price} on {date}, Gain/Loss: {gain_loss}")

        return self.balance, self.total_return, self.trades

# Ensure you've already instantiated the historical data as a DataFrame, for example:
historical_data = dm.loadData()  # Assuming `dm.loadData()` loads your data correctly.

# Create an instance of SMABacktest
sma_backtest = SMABacktest(historical_data, symbol="AAPL")

# Now call the backtest method on the instance
result = sma_backtest.run()  # or sma_backtest.backtest() if you are testing that directly
print(result)
>>>>>>> 9dd8bf2 (Added inheritance rules and fixed SMA)

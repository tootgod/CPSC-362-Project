# sma_backtest.py

from Backtest import Backtest
import pandas as pd  
from datetime import datetime
import csv


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

            # Buy signal: short SMA crosses above long SMA
            if short_sma[i] > long_sma[i] and short_sma[i - 1] <= long_sma[i - 1] and self.position == 0:
                self.position = 1
                self.shares = self.balance // price
                transaction_amount = self.shares * price
                self.balance -= transaction_amount
                self.trades.append((date, 'Buy', self.symbol, price, self.shares, transaction_amount, 0, self.balance, self.total_return))
                print(f"Buying at {price} on {date}")

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
#historical_data = dm.loadData()  # Assuming `dm.loadData()` loads your data correctly.

# Create an instance of SMABacktest
#sma_backtest = SMABacktest(historical_data, symbol="AAPL")

# Now call the backtest method on the instance
#result = sma_backtest.run()  # or sma_backtest.backtest() if you are testing that directly
#print(result)

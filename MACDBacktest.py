from Backtest import Backtest
import pandas as pd  
from datetime import datetime
import csv
import DataManager as dm

class MACDBacktest(Backtest):
    def calculate_macd(self, short_window=12, long_window=26, signal_window=9):
        short_ema = self.closes.ewm(span=short_window, adjust=False).mean()
        long_ema = self.closes.ewm(span=long_window, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        return macd_line, signal_line

    def backtest(self, short_window=12, long_window=26, signal_window=9):
        macd_line, signal_line = self.calculate_macd(short_window, long_window, signal_window)
        
        for i in range(1, len(macd_line)):
            date = self.dates.iloc[i]
            price = self.closes.iloc[i]
            
            # Buy signal: MACD line crosses above Signal line
            if macd_line[i] > signal_line[i] and macd_line[i - 1] <= signal_line[i - 1] and self.position == 0:
                self.position = 1
                self.shares = self.balance // price
                transaction_amount = self.shares * price
                self.balance -= transaction_amount
                self.trades.append((date, 'Buy', self.symbol, price, self.shares, transaction_amount, 0, self.balance, self.total_return))
                print(f"Buying at {price} on {date}")

            # Sell signal: MACD line crosses below Signal line
            elif macd_line[i] < signal_line[i] and macd_line[i - 1] >= signal_line[i - 1] and self.position == 1:
                self.position = 0
                transaction_amount = self.shares * price
                gain_loss = transaction_amount - self.trades[-1][5]
                self.balance += transaction_amount
                self.total_return = ((self.balance - self.initial_balance) / self.initial_balance) * 100
                self.trades.append((date, 'Sell', self.symbol, price, self.shares, transaction_amount, gain_loss, self.balance, self.total_return))
                print(f"Selling at {price} on {date}, Gain/Loss: {gain_loss}")

        return self.balance, self.total_return, self.trades


historical_data = dm.loadData()  # Assuming `dm.loadData()` loads your data correctly.

# Create an instance of SMABacktest
macd_backtest = MACDBacktest(historical_data, symbol="MACD")

# Now call the backtest method on the instance
result = macd_backtest.run()  # or sma_backtest.backtest() if you are testing that directly
print(result)


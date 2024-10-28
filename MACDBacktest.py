import pandas as pd
import csv

class MACDBacktest:
    def __init__(self, historical_data, initial_balance=100000):
        # Convert closes to a Pandas Series
        self.closes = pd.Series(historical_data['Close'])
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # Tracks current holding status: 0 (no stock), 1 (holding stock)
        self.trades = []   # Log of each trade: (buy/sell, price, date)
    
    def calculate_macd(self, short_window=12, long_window=26, signal_window=9):
        # Calculate short-term and long-term EMAs
        short_ema = self.closes.ewm(span=short_window, adjust=False).mean()
        long_ema = self.closes.ewm(span=long_window, adjust=False).mean()
        
        # MACD line and Signal line calculations
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        
        return macd_line, signal_line

    def backtest_macd(self):
        macd_line, signal_line = self.calculate_macd()
        
        for i in range(1, len(macd_line)):
            # Buy signal: MACD line crosses above Signal line
            if macd_line[i] > signal_line[i] and macd_line[i - 1] <= signal_line[i - 1] and self.position == 0:
                self.position = 1
                self.trades.append(('Buy', self.closes[i], i))
                print(f"Buying at {self.closes[i]} on day {i}")

            # Sell signal: MACD line crosses below Signal line
            elif macd_line[i] < signal_line[i] and macd_line[i - 1] >= signal_line[i - 1] and self.position == 1:
                self.position = 0
                trade_profit = self.closes[i] - self.trades[-1][1]
                self.balance += trade_profit
                self.trades.append(('Sell', self.closes[i], i))
                print(f"Selling at {self.closes[i]} on day {i}, Trade Profit: {trade_profit}")

        # Calculate total return
        total_return = ((self.balance - self.initial_balance) / self.initial_balance) * 100
        return self.balance, total_return, self.trades

    def run(self):
        final_balance, percent_return, trade_log = self.backtest_macd()
        summary = {
            "final_balance": final_balance,
            "percent_return": percent_return,
            "trade_log": trade_log
        }
        return summary
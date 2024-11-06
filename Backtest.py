import pandas as pd
from datetime import datetime
import csv

class Backtest:
    def __init__(self, historical_data, symbol, initial_balance=100000):
        # Ensure historical_data is a DataFrame
        if isinstance(historical_data, dict):
            historical_data = pd.DataFrame(historical_data)
        elif isinstance(historical_data, pd.Series):
            historical_data = historical_data.to_frame()

        # Ensure DataFrame has a 'Date' column
        if 'Date' not in historical_data.columns:
            historical_data.reset_index(inplace=True)
            historical_data.rename(columns={'index': 'Date'}, inplace=True)

        # Convert 'Date' column to datetime
        historical_data['Date'] = pd.to_datetime(historical_data['Date'], errors='coerce',unit='ms')

        # Initialize variables
        self.dates = historical_data['Date']
        self.closes = historical_data['Close']
        self.symbol = symbol
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0
        self.trades = []
        self.total_return = 0
        self.historical_data = historical_data.reset_index(drop=True)

    def backtest(self):
        raise NotImplementedError("Subclasses must implement the backtest method")

    def save_to_csv(self, filename="trade_log.csv"):
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([f"Backtest: Logged on {timestamp}"])
            writer.writerow(["Date", "Action", "Symbol", "Price", "Shares", "Transaction Amount", "$ Gain/Loss", "Balance", "Total Return"])
            for trade in self.trades:
                writer.writerow(trade)

    def run(self):
        final_balance, percent_return, trade_log = self.backtest()
        self.save_to_csv()
        summary = {
            "final_balance": final_balance,
            "percent_return": percent_return,
            "trade_log": trade_log
        }
        return summary
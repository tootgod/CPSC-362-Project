import pandas as pd  
from datetime import datetime
import csv

class MACDBacktest:
    def __init__(self, historical_data, symbol, initial_balance=100000):
        self.datesList = [int(date) / 1000 for date in historical_data['Close'].keys()]
        #ensure historical_data is a DataFrame
        if isinstance(historical_data, dict):
            historical_data = pd.DataFrame(historical_data)
        elif isinstance(historical_data, pd.Series):
            historical_data = historical_data.to_frame()

        #check the initial DataFrame structure
        #print("Initial DataFrame structure:")
        #print(historical_data.head())

        #if the DataFrame has no explicit index, use the index as the 'Date'
        if 'Date' not in historical_data.columns:
            historical_data.reset_index(inplace=True)
            historical_data.rename(columns={'index': 'Date'}, inplace=True)

        #ensure 'Date' is a Series and check for its type
        if not isinstance(historical_data['Date'], pd.Series):
            raise ValueError("historical_data must have a 'Date' column as a Series.")

        #convert the 'Date' column to datetime
        historical_data['Date'] = pd.to_datetime(pd.to_numeric(historical_data['Date']), unit='ms', errors='coerce')

        #check for any conversion issues
        if historical_data['Date'].isnull().any():
            print("Warning: Some dates could not be converted. Check your data.")

        #print the DataFrame after conversion
        #print("DataFrame after Date conversion:")
        #print(historical_data.head())

        #initialization of local variables
        self.dates = historical_data['Date']  #directly reference the column
        self.closes = historical_data['Close']
        self.symbol = symbol
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0
        self.trades = []
        self.annual_return = 0
        self.total_return = 0
        self.historical_data = historical_data.reset_index(drop=True)

    def calculate_macd(self, short_window=12, long_window=26, signal_window=9):
        short_ema = self.closes.ewm(span=short_window, adjust=False).mean()
        long_ema = self.closes.ewm(span=long_window, adjust=False).mean()
        
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        
        return macd_line, signal_line

    def backtest_macd(self):
        macd_line, signal_line = self.calculate_macd()
        transactionDatesBuy = []
        transactionDatesSell = []
        transactionHeightBuy = []
        transactionHeightSell = []
        for i in range(1, len(macd_line)):
            date = self.dates.iloc[i]  #iloc to access the correct index
            price = self.closes.iloc[i] 
            
            
            #buy signal: MACD line crosses above Signal line
            if macd_line[i] > signal_line[i] and macd_line[i - 1] <= signal_line[i - 1] and self.position == 0:
                self.position = 1
                self.shares = self.balance // price
                transaction_amount = self.shares * price
                transactionDatesBuy.append(self.datesList[i])
                transactionHeightBuy.append(macd_line[i])
                self.balance -= transaction_amount
                self.trades.append((date, 'Buy', self.symbol, price, self.shares, transaction_amount, 0, self.balance, self.total_return))
                #print(f"Buying at {price} on {date}")

            #sell signal: MACD line crosses below Signal line
            elif macd_line[i] < signal_line[i] and macd_line[i - 1] >= signal_line[i - 1] and self.position == 1:
                self.position = 0
                transaction_amount = self.shares * price
                transactionDatesSell.append(self.datesList[i])
                transactionHeightSell.append(macd_line[i])
                gain_loss = transaction_amount - self.trades[-1][5]
                self.balance += transaction_amount
                self.total_return = ((self.balance - self.initial_balance) / self.initial_balance) * 100
                self.trades.append((date, 'Sell', self.symbol, price, self.shares, transaction_amount, gain_loss, self.balance, self.total_return))
                #print(f"Selling at {price} on {date}, Gain/Loss: {gain_loss}")

        return self.balance, self.total_return, self.trades, transactionDatesSell,transactionDatesBuy, transactionHeightSell,transactionHeightBuy

    def save_to_csv(self, filename="MacD_trade_log.csv"):
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([f"MACD Backtest: Logged on {timestamp}"])
            writer.writerow(["Date", "Action", "Symbol", "Price", "Shares", "Transaction Amount", "$ Gain/Loss", "Balance", "Annual Return", "Total Return"])
            
            for trade in self.trades:
                writer.writerow(trade)

    def run(self):
        final_balance, percent_return, trade_log,transactionDatesBuy,transactionDatesSell, transactionHeightBuy,transactionHeightSell = self.backtest_macd()
        self.save_to_csv()
        summary = {
            "final_balance": final_balance,
            "percent_return": percent_return,
            "trade_log": trade_log
        }
        return summary, transactionDatesBuy,transactionDatesSell,transactionHeightBuy,transactionHeightSell
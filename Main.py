import DataManager as dm
from datetime import datetime, timedelta
import os
import dearpygui.dearpygui as dpg

#libraries like pandas and numpy to handle data and calculations
import pandas as pd
import numpy as np
import csv

# Initial Balance
initial_balance = 100000
balance = initial_balance
shares_held = 0
trade_log = []

historical_data = None
historical_dates = []
historical_closes = []
historical_highs = []
historical_lows = []
historical_opens = []
graphLabel = "Loaded Data"

# CSV log setup
# Trades and final summary are logged in a CSV file
csv_file = 'trade_log.csv'

#load historical data
def setupHistoricalData():
    global historical_data, historical_dates, historical_closes, historical_highs, historical_lows, historical_opens
    historical_data = dm.loadData()
    historical_dates = dm.getJsonDates(historical_data)
    historical_closes = dm.getJsonCloses(historical_data)
    historical_highs = dm.getJsonHighs(historical_data)
    historical_lows = dm.getJsonLows(historical_data)
    historical_opens = dm.getJsonOpens(historical_data)
    
#download FNGU data and load it
def setupFNGU():
    global graphLabel
    graphLabel = "FNGU"
    dm.downloadFNGU()
    if os.path.exists('historical_data.json'):
        setupHistoricalData()
    else:
        print("Error: File not found")
#download FNGD data and load it
def setupFNGD():
    global graphLabel
    graphLabel = "FNGD"
    dm.downloadFNGD()
    if os.path.exists('historical_data.json'):
        setupHistoricalData()
    else:
        print("Error: File not found")
    
# Calculate Simple Moving Average
#to compute short-term (50-day) and long-term (200-day) SMAs using pandas' rolling function.
def calculate_sma(data, window):
    return data.rolling(window=window).mean()

# Perform backtest using SMA cross-over strategy
# to simulate buy/sell actions based on SMA crossovers.
# It checks for crossovers between the short-term and long-term SMAs
# and performs trades accordingly.
def backtest_sma():
    global balance, shares_held, trade_log

    # Convert data to pandas dataframe for easier manipulation
    df = pd.DataFrame({
        'Date': pd.to_datetime(historical_dates),
        'Close': historical_closes
    })

    # Calculate 50-day and 200-day SMAs
    df['SMA50'] = calculate_sma(df['Close'], 50)
    df['SMA200'] = calculate_sma(df['Close'], 200)

    # Backtest logic
    for i in range(1, len(df)):
        date = df['Date'].iloc[i]
        price = df['Close'].iloc[i]
        sma50 = df['SMA50'].iloc[i]
        sma200 = df['SMA200'].iloc[i]

        # Buy signal: Short SMA crosses above Long SMA
        if df['SMA50'].iloc[i - 1] < df['SMA200'].iloc[i - 1] and sma50 > sma200 and shares_held == 0:
            shares_bought = balance // price
            transaction_amount = shares_bought * price
            balance -= transaction_amount
            shares_held = shares_bought
            log_trade(date, 'BUY', price, shares_bought, transaction_amount, 0)

        # Sell signal: Short SMA crosses below Long SMA
        elif df['SMA50'].iloc[i - 1] > df['SMA200'].iloc[i - 1] and sma50 < sma200 and shares_held > 0:
            transaction_amount = shares_held * price
            gain_loss = transaction_amount - (shares_held * df['Close'].iloc[i - 1])
            balance += transaction_amount
            log_trade(date, 'SELL', price, shares_held, transaction_amount, gain_loss)
            shares_held = 0

    # Final sell if shares are still held
    final_price = df['Close'].iloc[-1]
    if shares_held > 0:
        transaction_amount = shares_held * final_price
        gain_loss = transaction_amount - (shares_held * df['Close'].iloc[-2])
        balance += transaction_amount
        log_trade(df['Date'].iloc[-1], 'SELL (Final)', final_price, shares_held, transaction_amount, gain_loss)
        shares_held = 0

    # Calculate and log final summary
    total_gain_loss = balance - initial_balance
    days = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days
    annual_return = ((1 + total_gain_loss / initial_balance) ** (365 / days) - 1) * 100
    total_return = (balance - initial_balance) / initial_balance * 100
    log_summary(total_gain_loss, annual_return, total_return)
    
# Log each trade in the CSV
def log_trade(date, action, price, shares, transaction_amount, gain_loss):
    global trade_log
    trade_log.append([date, action, price, shares, transaction_amount, gain_loss, balance])

# Log the final summary in the CSV
# this includes total gain/loss, annual return, total return
def log_summary(total_gain_loss, annual_return, total_return):
    global trade_log
    trade_log.append(["SUMMARY", "", "", "", "", total_gain_loss, balance, annual_return, total_return])
    
        # Write log to CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Action', 'Price', 'Shares', 'Transaction Amount', 'Gain/Loss', 'Balance'])
        writer.writerows(trade_log)
    print(f"Trade log saved to {csv_file}")


# Check if json exists and load it if it does
if os.path.exists('historical_data.json'):
    setupHistoricalData()
    
# Create context for DearPyGui
dpg.create_context()

#Display the graph
def show_graph():
    close_graph()
    with dpg.window(label=graphLabel, width=950, height=675,no_title_bar=True,no_collapse=True,pos=[200,0],no_resize=True,no_move=True,tag="Historical Data"):

        def toggle_line_graph():
            dpg.configure_item(line_graph, show=not dpg.get_item_configuration(line_graph)["show"])
        def toggle_candle_graph():
            dpg.configure_item(candle_graph, show=not dpg.get_item_configuration(candle_graph)["show"])
        with dpg.menu(label="Graph Options"):
            dpg.add_menu_item(label="Toggle Line Graph", callback=toggle_line_graph)
            dpg.add_menu_item(label="Toggle Candle Graph", callback=toggle_candle_graph)
            dpg.add_menu_item(label="Close Graph", callback=close_graph)
        with dpg.plot(label="Closing Prices", height=600, width=900):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Date",time=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Price")
            dpg.set_axis_limits_auto(y_axis)
        
            
            line_graph = dpg.add_line_series(historical_dates, historical_closes, parent=y_axis,label = "Line Data")
            candle_graph = dpg.add_candle_series(historical_dates, historical_opens,historical_closes ,historical_lows, historical_highs, parent=y_axis,show=True,tooltip=True,label="Candle Data")
        
        #buttonShowLineGraph = dpg.add_button(label="Toggle Line Graph", callback=toggle_line_graph,pos=[800,0])
        #buttonShowCandleGraph = dpg.add_button(label="Toggle Candle Graph", callback=toggle_candle_graph)
        

def close_graph():
    if dpg.does_item_exist("Historical Data"):
        dpg.delete_item("Historical Data")
       
    
#buttons to download data and turn graph on. Should mostly be setup stuff like graph range and such.
if os.path.exists('historical_data.json'):
    show_graph()
with dpg.window(tag="Primary Window",width = 1100):
    def on_button_fngu():
        setupFNGU()
        show_graph()
        backtest_sma() # trigger the SMA backtest
    
    def on_button_fngd():
        setupFNGD()
        show_graph()
        backtest_sma()  trigger the SMA backtest

    buttonFngu = dpg.add_button(label="Download FNGU Data",callback=on_button_fngu)
    buttonFngd = dpg.add_button(label="Download FNGD Data",callback=on_button_fngd)
    
dpg.create_viewport(title='Trading Data', width=1168, height=705)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()


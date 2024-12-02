import pandas as pd
import SmaBacktest as sma

def BB_backtest(sec, period=20, symbol='BB', initial_balance=100000, std_dMult=0.8):
    # Load dates and close prices from a Security object
    dates = sec.historical_dates
    closes = sec.historical_closes

    # Convert data to pandas DataFrame
    df = pd.DataFrame({
        'Date': pd.to_datetime(dates,unit='s'), # Convert Unix timestamps to datetime
        'DateUnix': dates,
        'Close': closes
    })
    df.set_index('Date', inplace=True)

    # Calculate middle line (SMA) and standard deviation for the Bollinger Bands
    df['MiddleLine'] = sma.calculate_sma(df['Close'], period)
    df['StdDeviation'] = df['Close'].rolling(window=period).std()
    df['UpperBand'] = df['MiddleLine'] + (df['StdDeviation'] * std_dMult)
    df['LowerBand'] = df['MiddleLine'] - (df['StdDeviation'] * std_dMult)

    # Initialize backtest variables
    balance = initial_balance
    shares_held = 0
    trade_log = []

    # Initialize holding period
    threshold_percent = 0.05  # Smaller threshold for tighter conditions
    holding_period = 1  # Minimum holding period to allow quick trades

    # Initialize trend variables and days_since_buy
    trend_up = False
    trend_down = False
    days_since_buy = 0  # Initialize holding period counter

    balanceList = [initial_balance]
    num = [0]

    #variables for the trade graph
    transactionDatessell = []
    transactionDatesbuy = []
    transactionHeightsell = []
    transactionHeightbuy = []

    # Begin backtesting, starting only after `period` rows to avoid NaN values
    for i in range(period, len(df)):
        date = df.index[i]
        price = df['Close'].iloc[i]
        upper = df['UpperBand'].iloc[i]
        lower = df['LowerBand'].iloc[i]
        mid_line = df['MiddleLine'].iloc[i]

        # Determine trend direction
        if i > period:
            trend_up = df['MiddleLine'].iloc[i] > df['MiddleLine'].iloc[i - 1]
            trend_down = df['MiddleLine'].iloc[i] < df['MiddleLine'].iloc[i - 1]

        # Print values for debugging purposes
        print(f"\nDate: {date}, Price: {price}, LowerBand: {lower}, UpperBand: {upper}, MiddleLine: {mid_line}")

        # Test and print details about the buy condition
        if price < lower * (1 - threshold_percent):
            print(f"  - Potential BUY: Price below lower band on {date}")

        if shares_held == 0:
            print("  - No shares currently held.")

        if trend_up:
            print(f"  - Upward trend detected on {date}")

        # Buy Signal
        if price < lower * (1 - threshold_percent) and shares_held == 0 :
            shares_bought = balance // price
            transaction_amount = shares_bought * price
            balance -= transaction_amount
            balanceList.append(balanceList[-1] + (transaction_amount *-1))
            num.append(num[-1]+1)
            shares_held = shares_bought
            days_since_buy = 0  # Reset holding period after buy
            transactionDatesbuy.append(int(df['DateUnix'].iloc[i]))
            transactionHeightbuy.append(df['MiddleLine'].iloc[i])

            sma.log_trade(trade_log, date, 'BUY', symbol, price, shares_bought, transaction_amount, balance)
            print(f"  - Executing BUY on {date} at price {price}")

        # Test and print details about the sell condition
        if price > upper * (1 + threshold_percent):
            print(f"  - Potential SELL: Price above upper band on {date}")

        if shares_held > 0:
            print("  - Shares currently held.")

        if trend_down:
            print(f"  - Downward trend detected on {date}")

        # Sell Signal
        if price > upper * (1 + threshold_percent) and shares_held > 0 :
            transaction_amount = shares_held * price
            gain_loss = transaction_amount - (shares_held * df['Close'].iloc[i - 1])  # Calculate based on previous close
            balance += transaction_amount
            balanceList.append(balanceList[-1] + transaction_amount)
            num.append(num[-1]+1)
            transactionDatessell.append(int(df['DateUnix'].iloc[i]))
            transactionHeightsell.append(df["MiddleLine"].iloc[i])
            sma.log_trade(trade_log, date, 'SELL', symbol, price, shares_held, transaction_amount, balance, gain_loss)
            shares_held = 0  # Reset shares held after selling
            days_since_buy = 0  # Reset holding period after sell
            print(f"  - Executing SELL on {date} at price {price}")

        # Update holding period days if shares are held
        if shares_held > 0:
            days_since_buy += 1
    # Final sell if shares are still held
    if shares_held > 0:
        final_price = df['Close'].iloc[-1]
        transaction_amount = shares_held * final_price
        gain_loss = transaction_amount - (shares_held * df['Close'].iloc[-2])
        balance += transaction_amount
        balanceList.append(balanceList[-1] + transaction_amount)
        num.append(num[-1]+1)
        sma.log_trade(trade_log, df.index[-1], 'SELL (Final)', symbol, final_price, shares_held, transaction_amount, balance, gain_loss)
        shares_held = 0
        print(f"Logged final SELL trade on {df.index[-1]} at price {final_price}")

    # Calculate summary statistics
    total_gain_loss = balance - initial_balance
    days = (df.index[-1] - df.index[0]).days
    annual_return = ((1 + total_gain_loss / initial_balance) ** (365 / days) - 1) * 100 if days != 0 else 0
    total_return = (balance - initial_balance) / initial_balance * 100

    # Log summary
    sma.log_summary(trade_log, total_gain_loss, annual_return, total_return, balance)

    # Debug: print trade log to ensure it has content before saving
    print("Final trade_log for BB_backtest:", trade_log)

    # Save trade log to CSV
    print("Attempting to save trade log...")
    sma.save_trade_log(trade_log, f'{symbol}_trade_log.csv')
    print("Trade log saved successfully.")
    return balance, total_gain_loss, annual_return, total_return, balanceList, num, df['MiddleLine'].to_list(), df['UpperBand'].to_list(), df['LowerBand'].to_list(),transactionDatesbuy,transactionDatessell,transactionHeightbuy,transactionHeightsell


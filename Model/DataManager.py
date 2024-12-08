import yfinance as yf
import json
from datetime import datetime

#downloads Ticker data and saves it to a json file with a set start range
def downloadTicker(start_date,ticker):
    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')
    fngu_data = yf.download(ticker, start=start_date, end=end_date)
    fngu_data.to_json('historical_data.json')

#loads the json data from the file
def loadData():
    return json.load(open('historical_data.json', 'r'))

#returns a list of dates from the json data in Unix time
def getJsonDates(data):
   return [int(date) / 1000 for date in data['Close'].keys()]

#returns a list of daily closing prices from the json data
def getJsonCloses(data):
    lists = list(data['Close'].values())
    return lists

#returns a list of daily highs from the json data
def getJsonHighs(data):
    lists = list(data['High'].values())
    return lists

#returns a list of daily lows from the json data
def getJsonLows(data):
    lists = list(data['Low'].values())
    return lists

#returns a list of daily opens from the json data
def getJsonOpens(data):
    lists = list(data['Open'].values())
    return lists

def humanJson():
    # Define the tickers and date range
    tickers = ["FNGU", "FNGD"]
    start_date = "2020-01-01"
    end_date = "2024-11-02"

    # Step 1: Download data for both tickers, including all relevant columns
    data= yf.download(tickers, start=start_date, end=end_date)[["Open", "High", "Low", "Close", "Volume"]]

    # Step 2: Separate the data for each ticker
    fngu_data = data.xs('FNGU', level=1, axis=1).copy()
    fngd_data = data.xs('FNGD', level=1, axis=1).copy()

    # Reset index and convert dates
    fngu_data.reset_index(inplace=True)
    fngd_data.reset_index(inplace=True)
    fngu_data['Date'] = fngu_data['Date'].dt.strftime('%Y-%m-%d')
    fngd_data['Date'] = fngd_data['Date'].dt.strftime('%Y-%m-%d')

    # Convert to JSON format
    output_data = {
        "FNGU": fngu_data.to_dict(orient="records"),
        "FNGD": fngd_data.to_dict(orient="records")
    }

    # Save to JSON file
    with open("readableHistoricalData.json", "w") as f:
        json.dump(output_data, f, indent=4)
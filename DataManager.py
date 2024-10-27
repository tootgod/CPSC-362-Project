import yfinance as yf
import json
from datetime import datetime

#downloads FNGU data and saves it to a json file with a set start range
def downloadFNGU(start_date):
    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')
    fngu_data = yf.download('FNGU', start=start_date, end=end_date)
    fngu_data.to_json('historical_data.json')

#downloads FNGD data and saves it to a json file with a set start range
def downloadFNGD(start_date):
    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')
    fngd_data = yf.download('FNGD', start=start_date, end=end_date)
    fngd_data.to_json('historical_data.json')

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
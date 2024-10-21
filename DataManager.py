import yfinance as yf
import json
from datetime import datetime, timedelta
import pandas as pd

def downloadFNGU():
    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')
    fngu_data = yf.download('FNGU', start='2020-01-01', end=end_date)
    fngu_data.to_json('historical_data.json')

def downloadFNGD():
    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')
    fngd_data = yf.download('FNGD', start='2020-01-01', end=end_date)
    fngd_data.to_json('historical_data.json')

def loadData():
    return json.load(open('historical_data.json', 'r'))

def getJsonDates(data):
   return [int(date) / 1000 for date in data['Close'].keys()]

def getJsonCloses(data):
    lists = list(data['Close'].values())
    return lists

def getJsonHighs(data):
    lists = list(data['High'].values())
    return lists

def getJsonLows(data):
    lists = list(data['Low'].values())
    return lists

def getJsonOpens(data):
    lists = list(data['Open'].values())
    return lists
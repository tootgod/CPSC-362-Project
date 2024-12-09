import yfinance as yf
import json
from datetime import datetime

#downloads Ticker data and saves it to a json file with a set start range
class DataManager:
    @staticmethod
    def downloadTicker(start_date,ticker):
        today = datetime.now()
        end_date = today.strftime('%Y-%m-%d')
        fngu_data = yf.download(ticker, start=start_date, end=end_date)
        fngu_data.to_json('historical_data.json')
    
    #loads the json data from the file
    @staticmethod
    def loadData():
        return json.load(open('historical_data.json', 'r'))
    
    #returns a list of dates from the json data in Unix time
    @staticmethod
    def getJsonDates(data):
        return [int(date) / 1000 for date in data['Close'].keys()]
    
    @staticmethod
    def getJsonCloses(data):
        return list(data['Close'].values())
    
    @staticmethod
    def getJsonHighs(data):
        return list(data['High'].values())
    
    @staticmethod
    def getJsonLows(data):
        return list(data['Low'].values())
    
    @staticmethod
    def getJsonOpens(data):
        return list(data['Open'].values())
    
    @staticmethod
    def humanJson():
        tickers = ["FNGU", "FNGD"]
        start_date = "2020-01-01"
        end_date = "2024-11-02"
    
        data = yf.download(tickers, start=start_date, end=end_date)[["Open", "High", "Low", "Close", "Volume"]]
    
        fngu_data = data.xs('FNGU', level=1, axis=1).copy()
        fngd_data = data.xs('FNGD', level=1, axis=1).copy()
    
        fngu_data.reset_index(inplace=True)
        fngd_data.reset_index(inplace=True)
        fngu_data['Date'] = fngu_data['Date'].dt.strftime('%Y-%m-%d')
        fngd_data['Date'] = fngd_data['Date'].dt.strftime('%Y-%m-%d')
    
        output_data = {
            "FNGU": fngu_data.to_dict(orient="records"),
            "FNGD": fngd_data.to_dict(orient="records")
        }
    
        with open("readableHistoricalData.json", "w") as f:
            json.dump(output_data, f, indent=4)


class DataManagerDecorator:
    def __init__(self):
        self.data_manager = DataManager()

    def downloadTicker(self, start_date, ticker):
        self.data_manager.downloadTicker(start_date, ticker)

    def loadData(self):
        return self.data_manager.loadData()

    def getJsonDates(self, data):
        return self.data_manager.getJsonDates(data)

    def getJsonCloses(self, data):
        return self.data_manager.getJsonCloses(data)

    def getJsonHighs(self, data):
        return self.data_manager.getJsonHighs(data)

    def getJsonLows(self, data):
        return self.data_manager.getJsonLows(data)

    def getJsonOpens(self, data):
        return self.data_manager.getJsonOpens(data)

    def humanJson(self):
        self.data_manager.humanJson()
    
    def downloadTicker(self, start_date, end_date, ticker):
        fngu_data = yf.download(ticker, start=start_date, end=end_date)
        fngu_data.to_json('historical_data.json')

    
   
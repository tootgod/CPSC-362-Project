import yfinance as yf
import json
from datetime import datetime
import abc

class DataManager:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def downloadTicker(start_date, ticker):
        pass

    @abc.abstractmethod
    def loadData():
        pass

    @abc.abstractmethod
    def getJsonDates(data):
        pass

    @abc.abstractmethod
    def getJsonCloses(data):
        pass

    @abc.abstractmethod
    def getJsonHighs(data):
        pass

    @abc.abstractmethod
    def getJsonLows(data):
        pass

    @abc.abstractmethod
    def getJsonOpens(data):
        pass

    @abc.abstractmethod
    def humanJson():
        pass

    

#downloads Ticker data and saves it to a json file with a set start range
class DataManagerYahooAdapter(DataManager):
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



class DataManagerDecorator(DataManagerYahooAdapter):
    data_manager = DataManagerYahooAdapter()

    @staticmethod
    def downloadTicker(start_date, ticker):
        DataManagerDecorator.data_manager.downloadTicker(start_date, ticker)
    @staticmethod
    def loadData():
        return DataManagerDecorator.data_manager.loadData()
    @staticmethod
    def getJsonDates(data):
        return DataManagerDecorator.data_manager.getJsonDates(data)
    @staticmethod
    def getJsonCloses(data):
        return DataManagerDecorator.data_manager.getJsonCloses(data)
    @staticmethod
    def getJsonHighs(data):
        return DataManagerDecorator.data_manager.getJsonHighs(data)
    @staticmethod
    def getJsonLows(data):
        return DataManagerDecorator.data_manager.getJsonLows(data)
    @staticmethod
    def getJsonOpens(data):
        return DataManagerDecorator.data_manager.getJsonOpens(data)
    

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
    
   
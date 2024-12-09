import Model.YFinanceAdaptor as dm
from datetime import datetime, timedelta
import random
import time
import threading

class security:
    
    def __init__(self, Date = 0,Ticker = "0"):
        if Ticker == "0":
            self.historical_data = dm.DataManager.loadData()
            self.historical_dates = dm.DataManager.getJsonDates(self.historical_data) #Historical dates is a list of unix timestamps. It is saved this way because it is easier to convert unix timestamps to datetime objects in pandas, but hard to do the reverse.
            self.historical_closes = dm.DataManager.getJsonCloses(self.historical_data)
            self.historical_highs = dm.DataManager.getJsonHighs(self.historical_data)
            self.historical_lows = dm.DataManager.getJsonLows(self.historical_data)
            self.historical_opens = dm.DataManager.getJsonOpens(self.historical_data)
            dm.DataManager.humanJson()
        else:
            dm.DataManager.downloadTicker(Date,Ticker)
            self.historical_data = dm.DataManager.loadData()
            self.historical_dates = dm.DataManager.getJsonDates(self.historical_data)
            self.historical_closes = dm.DataManager.getJsonCloses(self.historical_data)
            self.historical_highs = dm.DataManager.getJsonHighs(self.historical_data)
            self.historical_lows = dm.DataManager.getJsonLows(self.historical_data)
            self.historical_opens = dm.DataManager.getJsonOpens(self.historical_data)
            dm.DataManager.humanJson()
       
    def subscribe(self, callback):
        if not hasattr(self, 'subscribers'):
            self.subscribers = []
        self.subscribers.append(callback)
    
    def publish(self, data):
        if hasattr(self, 'subscribers'):
            for callback in self.subscribers:
                callback(data)

    def addRandomData(self):
        data = self.historical_data
        last_date = self.historical_dates[-1]
        new_date = last_date + 86400000
        last_close = self.historical_closes[-1]
        if last_close is not None:
            change_percent = random.uniform(-0.03, 0.03)
            new_close = last_close * (1 + change_percent)
        else:
            print("Uh oh")
            time.sleep(10)
            return None
        new_open = last_close
        data['Open'][new_date] = new_open
        data['Close'][new_date] = new_close
        new_high = max(new_open, new_close) * (1 + random.uniform(0, 0.02))
        new_low = min(new_open, new_close) * (1 - random.uniform(0, 0.02))
        data['High'][new_date] = new_high
        data['Low'][new_date] = new_low

        self.historical_data = data
        self.historical_opens.append(new_open)
        self.historical_closes.append(new_close)
        self.historical_highs.append(new_high)
        self.historical_lows.append(new_low)
        self.historical_dates.append(new_date)
    
        self.publish(self)

    def startAddingRandomData(self, interval=1):
        def run():
            while True:
                self.addRandomData()
                time.sleep(interval)
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

        
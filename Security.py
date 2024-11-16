import DataManager as dm

class security:
    
    def __init__(self, Date = 0,Ticker = "0"):
        if Ticker == "0":
            self.historical_data = dm.loadData()
            self.historical_dates = dm.getJsonDates(self.historical_data) #Historical dates is a list of unix timestamps. It is saved this way because it is easier to convert unix timestamps to datetime objects in pandas, but hard to do the reverse.
            self.historical_closes = dm.getJsonCloses(self.historical_data)
            self.historical_highs = dm.getJsonHighs(self.historical_data)
            self.historical_lows = dm.getJsonLows(self.historical_data)
            self.historical_opens = dm.getJsonOpens(self.historical_data)
            dm.humanJson()
        else:
            dm.downloadTicker(Date,Ticker)
            self.historical_data = dm.loadData()
            self.historical_dates = dm.getJsonDates(self.historical_data)
            self.historical_closes = dm.getJsonCloses(self.historical_data)
            self.historical_highs = dm.getJsonHighs(self.historical_data)
            self.historical_lows = dm.getJsonLows(self.historical_data)
            self.historical_opens = dm.getJsonOpens(self.historical_data)
            dm.humanJson()
    
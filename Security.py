import DataManager as dm

class security:
    
    def __init__(self, historical_data):
        self.historical_dates = dm.getJsonDates(historical_data)
        self.historical_closes = dm.getJsonCloses(historical_data)
        self.historical_highs = dm.getJsonHighs(historical_data)
        self.historical_lows = dm.getJsonLows(historical_data)
        self.historical_opens = dm.getJsonOpens(historical_data)
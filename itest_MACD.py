import unittest
import pandas as pd
from MACDBacktest import MACDBacktest

class TestMACDIntegration(unittest.TestCase):
    def setUp(self):
        #sample historical data
        self.historical_data = {
            'Date': [1577923200000, 1578009600000, 1578268800000],
            'Close': [10, 11, 12]
        }
        df = pd.DataFrame(self.historical_data)
        self.symbol = 'TEST'  #provide a test symbol
        self.macd_backtest = MACDBacktest(df, self.symbol)  #initialize MACDBacktest with the DataFrame and symbol

    def test_date_conversion(self):
        expected_dates = [pd.Timestamp('2020-01-02'), pd.Timestamp('2020-01-03'), pd.Timestamp('2020-01-06')]
        for expected, actual in zip(expected_dates, self.macd_backtest.dates):
            self.assertEqual(expected, actual)

    def test_backtest_macd_integration(self):
        #run the MACD calculation
        macd_line, signal_line = self.macd_backtest.calculate_macd()

        #debugging output
        print("Final MACD Line for Integration Test:", macd_line)
        print("Final Signal Line for Integration Test:", signal_line)

        #add assertions as needed based on your integration requirements
        self.assertIsNotNone(macd_line, "MACD Line should not be None")
        self.assertIsNotNone(signal_line, "Signal Line should not be None")

if __name__ == '__main__':
    unittest.main()
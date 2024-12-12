import unittest
import pandas as pd
from Model.MACDBacktest import MACDBacktest

class TestMACDBacktest(unittest.TestCase):
    def setUp(self):
        #sample data for testing
        self.test_data = {
            'Date': [1577923200000, 1578009600000, 1578268800000],
            'Close': [10, 11, 12]
        }
        df = pd.DataFrame(self.test_data)
        self.symbol = 'TEST'  #provide a test symbol due to args
        self.macd_backtest = MACDBacktest(df, self.symbol)  #initialize MACDBacktest with the DataFrame and symbol

    def test_date_conversion(self):
        expected_dates = [pd.Timestamp('2020-01-02'), pd.Timestamp('2020-01-03'), pd.Timestamp('2020-01-06')]
        for expected, actual in zip(expected_dates, self.macd_backtest.dates):
            self.assertEqual(expected, actual)

    def test_macd_calculation(self):
        #calculate MACD
        macd_line, signal_line = self.macd_backtest.calculate_macd()  #call your MACD calculation

        #expected MACD values based on your logic (update with actual expected values)
        expected_macd = [0, 0.07977, 0.22113]  #replace with correct expected values, rounded appropriately

        for i in range(len(expected_macd)):
            with self.subTest(i=i):
                #round both calculated and expected values
                calculated_macd = round(macd_line[i], 5)
                expected_value = round(expected_macd[i], 5)

                #debugging output
                print(f"Comparing MACD at index {i}: calculated={calculated_macd}, expected={expected_value}")
                
                #assert that the rounded values are equal
                self.assertEqual(calculated_macd, expected_value)

if __name__ == '__main__':
    unittest.main()
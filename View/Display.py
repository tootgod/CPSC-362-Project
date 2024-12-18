from datetime import datetime
from abc import ABC, abstractmethod
import os
import dearpygui.dearpygui as dpg
#import Model.SmaBacktest as sma
#import Model.MACDBacktest as MACD
#import Model.BBbacktest as BB
import Controller.Controller as Controller
import utest_MACD as utest_MACD
import itest_MACD as itest_MACD
import Security as Security
import unittest




class Display:
    def __init__(self):
        self.graphLabel = "Loaded Data"

    def startup(self):
        dpg.create_context()

        if os.path.exists('historical_data.json'):
            self.sec = Security.security()
            self.sec.subscribe(self.secObserver)
            self.show_graph()

        with dpg.window(tag="Primary Window",width = 1100):
            def on_button_fngu():
                self.sec.unsubscribe(self.secObserver)
                day = int(dpg.get_value(dayDropdown))
                month = int(dpg.get_value(monthDropdown))
                year = int(dpg.get_value(yearDropdown))
                date = datetime(year,month,day)
                self.setupTicker(date,"FNGU")
                self.show_graph()
                self.sec.subscribe(self.secObserver)
            
            def on_button_fngd():
                self.sec.unsubscribe(self.secObserver)
                day = int(dpg.get_value(dayDropdown))
                month = int(dpg.get_value(monthDropdown))
                year = int(dpg.get_value(yearDropdown))
                date = datetime(year,month,day)
                self.setupTicker(date,"FNGD")     
                self.show_graph()     
                self.sec.subscribe(self.secObserver)  

            def on_button_backtest():
                backtest = dpg.get_value(backtestDropdown)
                if backtest == "SMA":
                    self.backtestWindow(Controller.SMAStrategy())
                elif backtest == "BB":
                    self.backtestWindow(Controller.BBStrategy())
                elif backtest == "MACD":
                    self.backtestWindow(Controller.MACDStrategy())

            
            
            buttonFngu = dpg.add_button(label="Download FNGU Data",callback=on_button_fngu)
            buttonFngd = dpg.add_button(label="Download FNGD Data",callback=on_button_fngd)
            monthDropdown = dpg.add_combo(label="Month", items=["1","2","3","4","5","6","7","8","9","10","11","12"],default_value="1",width=50)
            dayDropdown = dpg.add_combo(label="Day", items=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"],default_value="1",width=50)
            yearDropdown = dpg.add_combo(label="Year", items=["2024","2023","2022","2021","2020","2019","2018"],default_value="2020",width=50)
            backtestDropdown = dpg.add_combo(label="Backtest", items=["SMA","BB","MACD"],default_value="SMA",width=50)
            backtestButton = dpg.add_button(label="Run Backtest",callback=on_button_backtest)
            numbergenButton = dpg.add_button(label="Toggle Data Generation",callback=self.genToggle)


        if os.path.exists('historical_data.json'):
            sec = Security.security()
            sec.subscribe(self.secObserver)
            self.show_graph()
        dpg.create_viewport(title='Trading Data', width=1168, height=705)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    #observer to watch for real-time price changes
    def secObserver(self, Data):
        self.sec = Data
        self.update_graph()
        
    #download Specified Ticker data and load it
    def setupTicker(self, date,ticker):
        self.graphLabel = ticker
        self.sec = Security.security(date,ticker)
        if os.path.exists('historical_data.json'):
            self.sec = Security.security(ticker)
        else:
            print("Error: File not found")
        

    #display the graph
    def show_graph(self):
        self.close_graph()
        with dpg.window(label=self.graphLabel, width=950, height=675, no_title_bar=True, no_collapse=True, pos=[200, 0], no_resize=True, no_move=True, tag="Historical Data"):
    
            def toggle_line_graph():
                dpg.configure_item(line_graph, show=not dpg.get_item_configuration(line_graph)["show"])
            def toggle_candle_graph():
                dpg.configure_item(candle_graph, show=not dpg.get_item_configuration(candle_graph)["show"])
            with dpg.menu(label="Graph Options"):
                dpg.add_menu_item(label="Toggle Line Graph", callback=toggle_line_graph)
                dpg.add_menu_item(label="Toggle Candle Graph", callback=toggle_candle_graph)
                dpg.add_menu_item(label="Close Graph", callback=self.close_graph)
            with dpg.plot(label="Closing Prices", height=600, width=900):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Date",time=True)
                y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Price")
                dpg.set_axis_limits_auto(y_axis)

            line_graph = dpg.add_line_series(self.sec.historical_dates, self.sec.historical_closes, parent=y_axis, label="Line Data",tag="Line Graph")
            candle_graph = dpg.add_candle_series(self.sec.historical_dates, self.sec.historical_opens, self.sec.historical_closes, self.sec.historical_lows, self.sec.historical_highs, parent=y_axis, show=True, tooltip=True, label="Candle Data",tag="Candle Graph")
            
    def genToggle(self):
        if self.sec.genning:
            self.sec.stopAddingRandomData()
        else:
            self.sec.startAddingRandomData()        

    def close_graph(self):
        if dpg.does_item_exist("Historical Data"):
            dpg.delete_item("Historical Data")


    def update_graph(self):
        if dpg.does_item_exist("Line Graph"):
            dpg.configure_item("Line Graph", y=self.sec.historical_closes, x=self.sec.historical_dates)
        if dpg.does_item_exist("Candle Graph"):
            dpg.configure_item("Candle Graph", opens=self.sec.historical_opens, closes=self.sec.historical_closes, lows=self.sec.historical_lows, highs=self.sec.historical_highs, dates=self.sec.historical_dates)

    def run_tests(self):
        # Discover and run tests from both test files
        loader = unittest.TestLoader()
        
        # Load test cases from both test files
        tests_1 = loader.loadTestsFromModule(utest_MACD)  # Adjust the import if needed
        tests_2 = loader.loadTestsFromModule(itest_MACD)  # Adjust the import if needed
        
        # Create a test suite
        suite = unittest.TestSuite([tests_1, tests_2])
        
        # Run the tests
        runner = unittest.TextTestRunner()
        results = runner.run(suite)


    def backtestWindow(self, strategy: Controller.TradingStrategy):
        results = strategy.getBacktestResults(self.sec)
        with dpg.window(label=strategy.getName(), width=950, height=700):
            strategy.plot(dpg, self.sec, results)

            
            self.run_tests()
                
        

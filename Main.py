import DataManager as dm
from datetime import datetime
import os
import dearpygui.dearpygui as dpg
import SmaBacktest as sma
import MACDBacktest as MACD
import utest_MACD as utest_MACD
import itest_MACD as itest_MACD
import Security
import unittest

historical_data = None
sec = None
graphLabel = "Loaded Data"

#load historical data
def setupHistoricalData():
    global historical_data, sec
    historical_data = dm.loadData()
    sec = Security.security(historical_data)
    
    
#download FNGU data and load it
def setupFNGU(date):
    global graphLabel
    graphLabel = "FNGU"
    dm.downloadFNGU(date)
    if os.path.exists('historical_data.json'):
        setupHistoricalData()
    else:
        print("Error: File not found")
#download FNGD data and load it
def setupFNGD(date):
    global graphLabel
    graphLabel = "FNGD"
    dm.downloadFNGD(date)
    if os.path.exists('historical_data.json'):
        setupHistoricalData()
    else:
        print("Error: File not found")
    

#check if json exists and load it if it does
if os.path.exists('historical_data.json'):
    setupHistoricalData()


   

dpg.create_context()

#display the graph
def show_graph():
    close_graph()
    with dpg.window(label=graphLabel, width=950, height=675, no_title_bar=True, no_collapse=True, pos=[200, 0], no_resize=True, no_move=True, tag="Historical Data"):
 
        def toggle_line_graph():
            dpg.configure_item(line_graph, show=not dpg.get_item_configuration(line_graph)["show"])
        def toggle_candle_graph():
            dpg.configure_item(candle_graph, show=not dpg.get_item_configuration(candle_graph)["show"])
        with dpg.menu(label="Graph Options"):
            dpg.add_menu_item(label="Toggle Line Graph", callback=toggle_line_graph)
            dpg.add_menu_item(label="Toggle Candle Graph", callback=toggle_candle_graph)
            dpg.add_menu_item(label="Close Graph", callback=close_graph)
        with dpg.plot(label="Closing Prices", height=600, width=900):
            dpg.add_plot_legend()
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Price")
            dpg.set_axis_limits_auto(y_axis)

            line_graph = dpg.add_line_series(sec.historical_dates, sec.historical_closes, parent=y_axis, label="Line Data")
            candle_graph = dpg.add_candle_series(sec.historical_dates, sec.historical_opens, sec.historical_closes, sec.historical_lows, sec.historical_highs, parent=y_axis, show=True, tooltip=True, label="Candle Data")
        
        

def close_graph():
    if dpg.does_item_exist("Historical Data"):
        dpg.delete_item("Historical Data")

def run_tests():
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

    # Print the test results
    print(f"Tests run: {results.testsRun}, Failures: {len(results.failures)}, Errors: {len(results.errors)}")


def backtestWindow(strat):
    with dpg.window(label=strat,width = 200,height=100):
        if strat == "SMA":
            sma.backtest_sma(historical_data)
            dpg.add_text("SMA Backtest Results")
            dpg.add_text("Total gain/loss: " + "0")
            dpg.add_text("% Return: " + "0")
        elif strat == "BB":
            dpg.add_text("BB Backtest Results")
            dpg.add_text("Total gain/loss: " + "0")
            dpg.add_text("% Return: " + "0")    
        elif strat == "MACD":
            # Run MACD Backtest
            macd_backtest = MACD.MACDBacktest(historical_data, symbol = "MACD")
            summary = macd_backtest.run()
            
            # Display MACD results in GUI
            dpg.add_text("MACD Backtest Results")
            dpg.add_text("Final Balance: $" + str(round(summary["final_balance"], 2)))
            dpg.add_text("Total % Return: " + str(round(summary["percent_return"], 2)) + "%")
            dpg.add_text("Trade Log:")
            for trade in summary["trade_log"]:
                dpg.add_text(f"{trade[0]}, Signal: {trade[1]}")    
            
            run_tests()
            
       
    
#buttons to download data and turn graph on. Should mostly be setup stuff like graph range and such.
if os.path.exists('historical_data.json'):
    show_graph()
with dpg.window(tag="Primary Window",width = 1100):
    def on_button_fngu():

        day = int(dpg.get_value(dayDropdown))
        month = int(dpg.get_value(monthDropdown))
        year = int(dpg.get_value(yearDropdown))
        date = datetime(year,month,day)
        setupFNGU(date)
        sma.backtest_sma(historical_data)
        show_graph()
    
    def on_button_fngd():

        day = int(dpg.get_value(dayDropdown))
        month = int(dpg.get_value(monthDropdown))
        year = int(dpg.get_value(yearDropdown))
        date = datetime(year,month,day)
        setupFNGD(date)
        sma.backtest_sma(historical_data)        
        show_graph()       

    def on_button_backtest():
        backtest = dpg.get_value(backtestDropdown)
        backtestWindow(backtest)
    
    
        

    buttonFngu = dpg.add_button(label="Download FNGU Data",callback=on_button_fngu)
    buttonFngd = dpg.add_button(label="Download FNGD Data",callback=on_button_fngd)
    monthDropdown = dpg.add_combo(label="Month", items=["1","2","3","4","5","6","7","8","9","10","11","12"],default_value="1",width=50)
    dayDropdown = dpg.add_combo(label="Day", items=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"],default_value="1",width=50)
    yearDropdown = dpg.add_combo(label="Year", items=["2024","2023","2022","2021","2020","2019","2018"],default_value="2020",width=50)
    backtestDropdown = dpg.add_combo(label="Backtest", items=["SMA","BB","MACD"],default_value="SMA",width=50)
    bacjtestButton = dpg.add_button(label="Run Backtest",callback=on_button_backtest)

dpg.create_viewport(title='Trading Data', width=1168, height=705)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
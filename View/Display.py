from datetime import datetime
import os
import dearpygui.dearpygui as dpg
import Controller.SmaBacktest as sma
import Controller.MACDBacktest as MACD
import Controller.BBbacktest as BB
import utest_MACD as utest_MACD
import itest_MACD as itest_MACD
import Model.Security as Security
import unittest

class Display:
    def __init__(self):
        self.graphLabel = "Loaded Data"

        #check if json exists and load it if it does
        if os.path.exists('historical_data.json'):
            self.sec = Security.security()
            self.sec.startAddingRandomData()
            
    
    def startup(self):
        dpg.create_context()

        if os.path.exists('historical_data.json'):
            self.show_graph()

        with dpg.window(tag="Primary Window",width = 1100):
            def on_button_fngu():

                day = int(dpg.get_value(dayDropdown))
                month = int(dpg.get_value(monthDropdown))
                year = int(dpg.get_value(yearDropdown))
                date = datetime(year,month,day)
                self.setupTicker(date,"FNGU")
                self.show_graph()
            
            def on_button_fngd():

                day = int(dpg.get_value(dayDropdown))
                month = int(dpg.get_value(monthDropdown))
                year = int(dpg.get_value(yearDropdown))
                date = datetime(year,month,day)
                self.setupTicker(date,"FNGD")     
                self.show_graph()       

            def on_button_backtest():
                backtest = dpg.get_value(backtestDropdown)
                self.backtestWindow(backtest)
            
            
                

            buttonFngu = dpg.add_button(label="Download FNGU Data",callback=on_button_fngu)
            buttonFngd = dpg.add_button(label="Download FNGD Data",callback=on_button_fngd)
            monthDropdown = dpg.add_combo(label="Month", items=["1","2","3","4","5","6","7","8","9","10","11","12"],default_value="1",width=50)
            dayDropdown = dpg.add_combo(label="Day", items=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"],default_value="1",width=50)
            yearDropdown = dpg.add_combo(label="Year", items=["2024","2023","2022","2021","2020","2019","2018"],default_value="2020",width=50)
            backtestDropdown = dpg.add_combo(label="Backtest", items=["SMA","BB","MACD"],default_value="SMA",width=50)
            backtestButton = dpg.add_button(label="Run Backtest",callback=on_button_backtest)

        dpg.create_viewport(title='Trading Data', width=1168, height=705)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()



    def secObserver(self, Data):
        self.sec = Data
        print("Data has been updated")
        self.show_graph()
        
    #download Specified Ticker data and load it
    def setupTicker(self, date,ticker):
        self.graphLabel = ticker
        self.sec = Security.security(date,ticker)
        self.sec.subscribe(self.secObserver)
        self.sec.startAddingRandomData()
        if os.path.exists('historical_data.json'):
            self.sec = Security.security(ticker)
        else:
            print("Error: File not found")
        

    #check if json exists and load it if it does
    #if os.path.exists('historical_data.json'):
    #    sec = Security.security()
    #    sec.startAddingRandomData()


    

    # dpg.create_context()

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

                line_graph = dpg.add_line_series(self.sec.historical_dates, self.sec.historical_closes, parent=y_axis, label="Line Data")
                candle_graph = dpg.add_candle_series(self.sec.historical_dates, self.sec.historical_opens, self.sec.historical_closes, self.sec.historical_lows, self.sec.historical_highs, parent=y_axis, show=True, tooltip=True, label="Candle Data")
            
            

    def close_graph(self):
        if dpg.does_item_exist("Historical Data"):
            dpg.delete_item("Historical Data")

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

        # Print the test results
        #print(f"Tests run: {results.testsRun}, Failures: {len(results.failures)}, Errors: {len(results.errors)}")


    def backtestWindow(self, strat):
        with dpg.window(label=strat,width = 950,height=700):
            if strat == "SMA":
                balance, total_gain_loss, annual_return, total_return,balanceList,num,smasmalllist,smabiglist,tdateB,tdateS,tHeightB,tHeightS = sma.backtest_sma(self.sec)

                dpg.add_text("SMA Backtest Results")
                dpg.add_text(f"Final Balance: ${balance:,.2f}")
                dpg.add_text(f"Total Gain/Loss: ${total_gain_loss:,.2f}")
                dpg.add_text(f"Annual Return: {annual_return:.2f}%")
                dpg.add_text(f"Total Return: {total_return:.2f}%")

                with dpg.plot(label="Closing Prices", height=600, width=900):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Trade number",time=True)
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Capital")
                    dpg.set_axis_limits_auto(y_axis)
                    dpg.add_scatter_series(tdateB,tHeightB,parent=y_axis, label="Buy Signal")
                    dpg.add_scatter_series(tdateS,tHeightS,parent=y_axis, label="Sell Signal")
                    dpg.add_line_series(self.sec.historical_dates,smasmalllist,parent=y_axis, label="SMA Long Data")
                    dpg.add_line_series(self.sec.historical_dates,smabiglist,parent=y_axis, label="SMA Short Data")
            elif strat == "BB":
                # Run BB_backtest and display results
                balance, total_gain_loss, annual_return, total_return,balanceList,num,mband,uband,lband,tDateB,tDateS,tHeightb,tHeightS = BB.BB_backtest(self.sec)
                dpg.add_text("BB Backtest Results")
                dpg.add_text(f"Final Balance: ${balance:,.2f}")
                dpg.add_text(f"Total Gain/Loss: ${total_gain_loss:,.2f}")
                dpg.add_text(f"Annual Return: {annual_return:.2f}%")
                dpg.add_text(f"Total Return: {total_return:.2f}%")
                with dpg.plot(label="Closing Prices", height=600, width=900):
                    dpg.add_plot_legend()

                    dpg.add_plot_axis(dpg.mvXAxis, label="Trade number",time=True)
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Capital")
                    dpg.set_axis_limits_auto(y_axis)

                    dpg.add_scatter_series(tDateB,tHeightb,parent=y_axis, label="Buy Signal")
                    dpg.add_scatter_series(tDateS,tHeightS,parent=y_axis, label="Sell Signal")
                    dpg.add_line_series(self.sec.historical_dates, self.sec.historical_closes, parent=y_axis, label="Closes")
                    dpg.add_line_series(self.sec.historical_dates,mband,parent=y_axis, label="Middle Band")
                    dpg.add_line_series(self.sec.historical_dates,uband,parent=y_axis, label="Upper Band")
                    dpg.add_line_series(self.sec.historical_dates,lband,parent=y_axis, label="Lower Band")
            elif strat == "MACD":
                # Run MACD Backtest
                print(self.sec)
                macd_backtest = MACD.MACDBacktest(self.sec, symbol = "MACD")
                summary ,tdateB,tdateS,tHeightB,tHeightS = macd_backtest.run()
                
                # Display MACD results in GUI
                dpg.add_text("MACD Backtest Results")
                dpg.add_text("Final Balance: $" + str(round(summary["final_balance"], 2)))
                dpg.add_text("Total % Return: " + str(round(summary["percent_return"], 2)) + "%")
                #dpg.add_text("Trade Log:")
                amnt = [100000]
                num = [0]
                for trade in summary["trade_log"]:
                    #dpg.add_text(f"{trade[0]}, Signal: {trade[1]}, Shares: {trade[4]}, Amount: ${trade[5]:,.2f}")
                    amnt.append(trade[5])
                    num.append(num[-1]+1)
                with dpg.plot(label="Closing Prices", height=600, width=900):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Trade number",time=True)
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Capital")
                    dpg.set_axis_limits_auto(y_axis)

                    #dpg.add_line_series(num, amnt, parent=y_axis, label="Line Data")
                    
                    macd_line, signal_line = macd_backtest.calculate_macd()
                    macd_line = macd_line.to_list()
                    signal_line = signal_line.to_list()
                    #print("tdate Line:")
                    #print(tdate)
                    #print("tHeight Line:")
                    #print(tHeight)
                    #dpg.add_line_series(sec.historical_dates, sec.historical_closes, parent=y_axis, label="Price")
                    dpg.add_scatter_series(tdateB,tHeightB,parent=y_axis, label="Buy Signal")
                    dpg.add_scatter_series(tdateS,tHeightS,parent=y_axis, label="Sell Signal")
                    dpg.add_line_series(self.sec.historical_dates, macd_line, parent=y_axis, label="MACD")  # Red for MACD line
                    dpg.add_line_series(self.sec.historical_dates, signal_line, parent=y_axis, label="Signal")  # Blue for Signal line
            
                self.run_tests()
                
        
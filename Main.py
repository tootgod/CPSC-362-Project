import DataManager as dm
from datetime import datetime, timedelta
import os
import dearpygui.dearpygui as dpg
historical_data = None
historical_dates = []
historical_closes = []
historical_highs = []
historical_lows = []
historical_opens = []
graphLabel = "Loaded Data"
date = datetime.now()

#load historical data
def setupHistoricalData():
    global historical_data, historical_dates, historical_closes, historical_highs, historical_lows, historical_opens
    historical_data = dm.loadData()
    historical_dates = dm.getJsonDates(historical_data)
    historical_closes = dm.getJsonCloses(historical_data)
    historical_highs = dm.getJsonHighs(historical_data)
    historical_lows = dm.getJsonLows(historical_data)
    historical_opens = dm.getJsonOpens(historical_data)
    
#download FNGU data and load it
def setupFNGU():
    global graphLabel
    graphLabel = "FNGU"
    dm.downloadFNGU(date)
    if os.path.exists('historical_data.json'):
        setupHistoricalData()
    else:
        print("Error: File not found")
#download FNGD data and load it
def setupFNGD():
    global graphLabel
    graphLabel = "FNGD"
    dm.downloadFNGD(date)
    if os.path.exists('historical_data.json'):
        setupHistoricalData()
    else:
        print("Error: File not found")
    

# Check if json exists and load it if it does
if os.path.exists('historical_data.json'):
    setupHistoricalData()
    
dpg.create_context()

#Display the graph
def show_graph():
    close_graph()
    with dpg.window(label=graphLabel, width=950, height=675,no_title_bar=True,no_collapse=True,pos=[200,0],no_resize=True,no_move=True,tag="Historical Data"):
 
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
            dpg.add_plot_axis(dpg.mvXAxis, label="Date",time=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Price")
            dpg.set_axis_limits_auto(y_axis)
        
            
            line_graph = dpg.add_line_series(historical_dates, historical_closes, parent=y_axis,label = "Line Data")
            candle_graph = dpg.add_candle_series(historical_dates, historical_opens,historical_closes ,historical_lows, historical_highs, parent=y_axis,show=True,tooltip=True,label="Candle Data")
        
        

def close_graph():
    if dpg.does_item_exist("Historical Data"):
        dpg.delete_item("Historical Data")
       
    
#buttons to download data and turn graph on. Should mostly be setup stuff like graph range and such.
if os.path.exists('historical_data.json'):
    show_graph()
with dpg.window(tag="Primary Window",width = 1100):
    def on_button_fngu():
        global date
        day = int(dpg.get_value(dayDropdown))
        month = int(dpg.get_value(monthDropdown))
        year = int(dpg.get_value(yearDropdown))
        date = datetime(year,month,day)
        setupFNGU()
        show_graph()
    
    def on_button_fngd():
        global date
        day = int(dpg.get_value(dayDropdown))
        month = int(dpg.get_value(monthDropdown))
        year = int(dpg.get_value(yearDropdown))
        date = datetime(year,month,day)
        setupFNGD()        
        show_graph()       
    
    
        

    buttonFngu = dpg.add_button(label="Download FNGU Data",callback=on_button_fngu)
    buttonFngd = dpg.add_button(label="Download FNGD Data",callback=on_button_fngd)
    monthDropdown = dpg.add_combo(label="Month", items=["1","2","3","4","5","6","7","8","9","10","11","12"],default_value="1",width=50)
    dayDropdown = dpg.add_combo(label="Day", items=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"],default_value="1",width=50)
    yearDropdown = dpg.add_combo(label="Year", items=["2024","2023","2022","2021","2020","2019","2018"],default_value="2020",width=50)

dpg.create_viewport(title='Trading Data', width=1168, height=705)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
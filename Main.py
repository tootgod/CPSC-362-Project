import DataManager as dm
from datetime import datetime, timedelta
import os
import dearpygui.dearpygui as dpg
historical_data = None
historical_dates = []
historical_closes = []
graphLabel = "Loaded Data"
# Check if json exists and load it if it does
def setupHistoricalData():
    global historical_data, historical_dates, historical_closes
    historical_data = dm.loadData()
    historical_dates = dm.getJsonDates(historical_data)
    historical_closes = dm.getJsonCloses(historical_data)
    

def setupFNGU():
    global graphLabel
    graphLabel = "FNGU"
    dm.downloadFNGU()
    if os.path.exists('historical_data.json'):
        setupHistoricalData()
    else:
        print("Error: File not found")

def setupFNGD():
    global graphLabel
    graphLabel = "FNGD"
    dm.downloadFNGD()
    if os.path.exists('historical_data.json'):
        setupHistoricalData()
    else:
        print("Error: File not found")
    


if os.path.exists('historical_data.json'):
    historical_data = dm.loadData()
    historical_dates = dm.getJsonDates(historical_data)
    historical_closes = dm.getJsonCloses(historical_data)

    
# Create DearPyGui context and viewport
dpg.create_context()
def show_graph():
    close_graph()
    with dpg.window(label=graphLabel, width=850, height=650,no_collapse=True,no_title_bar=True,pos=[200,0],no_resize=True,no_move=True,tag="Historical Data"):
        dpg.add_text("Closing Prices")
        with dpg.plot(label="Closing Prices", height=600, width=800):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Date")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Price")
            dpg.set_axis_limits(y_axis, 0, 25000)
        
            dpg.add_line_series(historical_dates, historical_closes, label="Data", parent=y_axis)
def close_graph():
    if dpg.does_item_exist("Historical Data"):
        dpg.delete_item("Historical Data")

if os.path.exists('historical_data.json'):
    show_graph()
with dpg.window(tag="Primary Window"):
    def on_button_fngu():
        setupFNGU()
    
    def on_button_fngd():
        setupFNGD()        

    buttonFngu = dpg.add_button(label="Download FNGU Data",callback=on_button_fngu)
    buttonFngd = dpg.add_button(label="Download FNGD Data",callback=on_button_fngd)
    buttonShowGraph = dpg.add_button(label="Show Graph", callback=show_graph)
dpg.create_viewport(title='Trading Data', width=1100, height=675)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
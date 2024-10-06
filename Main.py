import yfinance as yf
import json
from datetime import datetime, timedelta
import os

import dearpygui.dearpygui as dpg
# Download historical data for FNGU and FNGD

# Get the last market closing date
today = datetime.now()
if today.weekday() == 5:  # Saturday
    end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
elif today.weekday() == 6:  # Sunday
    end_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')
else:
    end_date = today.strftime('%Y-%m-%d')

def is_data_up_to_date(file_path, end_date):
    if not os.path.exists(file_path):
        return False
    with open(file_path, 'r') as f:
        data = json.load(f)
        last_date = max(int(date) for date in data['Close'].keys())
        last_date_str = datetime.fromtimestamp(last_date / 1000).strftime('%Y-%m-%d')
        print(last_date_str)
        print(end_date)
        print(last_date_str >= end_date)
        return last_date_str >= end_date

fngu_file = 'FNGU_historical_data.json'
fngd_file = 'FNGD_historical_data.json'

if not is_data_up_to_date(fngu_file, end_date):
    fngu_data = yf.download('FNGU', start='2020-01-01', end=end_date)
    fngu_data.to_json(fngu_file)

if not is_data_up_to_date(fngd_file, end_date):
    fngd_data = yf.download('FNGD', start='2020-01-01', end=end_date)
    fngd_data.to_json(fngd_file)


# Load the data from the JSON files and display the data in a graph in DearPyGui
# Load the data from the JSON files
with open('FNGU_historical_data.json', 'r') as f:
    fngu_data = json.load(f)

with open('FNGD_historical_data.json', 'r') as f:
    fngd_data = json.load(f)

# Extract dates and closing prices
fngu_dates = [int(date) / 1000 for date in fngu_data['Close'].keys()]
fngu_closes = list(fngu_data['Close'].values())

fngd_dates = [int(date) / 1000 for date in fngd_data['Close'].keys()]
fngd_closes = list(fngd_data['Close'].values())

# Create DearPyGui context and viewport
dpg.create_context()
dpg.create_viewport(title='Trading Data', width=850, height=700)

with dpg.window(label="FNGU and FNGD Historical Data", width=850, height=650):
    dpg.add_text("FNGU and FNGD Closing Prices")
    with dpg.plot(label="Closing Prices", height=600, width=800):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="Date")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Price")
        dpg.set_axis_limits(y_axis, 0, 25000)
        
        dpg.add_line_series(fngu_dates, fngu_closes, label="FNGU", parent=y_axis)
        dpg.add_line_series(fngd_dates, fngd_closes, label="FNGD", parent=y_axis)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
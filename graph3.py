import panel as pn
import pandas as pd
import hvplot.pandas
import holoviews as hv
import numpy as np

# Read the CSV data
# Read the CSV data
def read_csv_data(filepath):
    df = pd.read_csv(filepath, index_col=0)
    return df

# Calculate the average for each month
def calculate_monthly_averages(df):
    return df.mean(axis=1)




# Checkboxes for options panel
regular_checkbox = pn.widgets.Checkbox(name='Regular', value=True)
super_checkbox = pn.widgets.Checkbox(name='Super', value=True)
diesel_checkbox = pn.widgets.Checkbox(name='Diesel', value=True)

@pn.depends(regular_checkbox.param.value, super_checkbox.param.value, diesel_checkbox.param.value)
def create_plot(regular, super_fuel, diesel):
    plots = []
    
    if regular:
        df = read_csv_data('data/gasregularpormes.csv')
        monthly_averages = df.mean(axis=1, skipna=True)
        plots.append(hv.Bars(monthly_averages, label='Regular').opts(color='blue'))
        
    if super_fuel:
        df = read_csv_data('data/gassuperpormes.csv')
        monthly_averages = df.mean(axis=1, skipna=True)
        plots.append(hv.Bars(monthly_averages, label='Super').opts(color='green'))
        
    if diesel:
        df = read_csv_data('data/dieselpormes.csv')
        monthly_averages = df.mean(axis=1, skipna=True)
        plots.append(hv.Bars(monthly_averages, label='Diesel').opts(color='red'))
        
    if not plots:
        return hv.Bars([])  # Empty plot if none are selected
    
    overlay = hv.Overlay(plots).opts(width=600, xlabel='Month', ylabel='Average Value', title='Monthly Averages')
    return overlay

# Dropdown to select CSV file
csv_dropdown = pn.widgets.Select(name='Select CSV', options=['data/gasregularpormes.csv', 'data/gassuperpormes.csv', 'data/dieselpormes.csv'])

# Options panel
options_panel = pn.WidgetBox(
    "# Options",
    regular_checkbox,
    super_checkbox,
    diesel_checkbox,
    csv_dropdown
)

# Bind the create_plot function to the checkbox widgets and dropdown
bound_plot = pn.bind(create_plot, regular=regular_checkbox, super_fuel=super_checkbox, diesel=diesel_checkbox)

# Create a dynamic map to update the plot based on the checkbox values and selected CSV
dynamic_plot = hv.DynamicMap(bound_plot)

# Create a Panel app with the options panel on the left and the plot on the right
app = pn.Row(options_panel, dynamic_plot)

# Show the app
app.show()


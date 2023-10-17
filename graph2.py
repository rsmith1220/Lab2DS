import panel as pn
import pandas as pd
import hvplot.pandas
import holoviews as hv

# Data and labels
data = [25.49, 26.38, 22.26]
labels = ["Regular", "Super", "Diesel"]

# Read the CSV data
def read_csv_data(filepath):
    df = pd.read_csv(filepath, index_col=0)
    return df

# Calculate the average for each month
def calculate_monthly_averages(df):
    return df.mean(axis=1)

# Convert data to DataFrame for plotting
df = pd.DataFrame({
    'Tipo de gasolina': labels,
    'Amount': data
})
# Checkboxes for options panel
regular_checkbox = pn.widgets.Checkbox(name='Regular', value=True)
super_checkbox = pn.widgets.Checkbox(name='Super', value=True)
diesel_checkbox = pn.widgets.Checkbox(name='Diesel', value=True)
# Create a function to generate the bar plot based on the checkboxes
def create_plot(regular, super_fuel, diesel):
    filtered_df = df[df['Tipo de gasolina'].isin(
        [label for label, checkbox in zip(labels, [regular, super_fuel, diesel]) if checkbox]
    )]
    bar_plot = filtered_df.hvplot.bar(x='Tipo de gasolina', y='Amount', alpha=0.6, label='Promedio de gasolina por tipo', width=800)
    vline = hv.VLine(filtered_df['Amount'].mean()).opts(color='red', line_width=2)
    average_of_data = filtered_df['Amount'].mean()
    label = hv.Text(1, average_of_data + 1, f'Promedio total: {average_of_data:.2f}').opts(text_font_size='10pt', text_color='red')
    return bar_plot * vline * label

@pn.depends(regular_checkbox.param.value, super_checkbox.param.value, diesel_checkbox.param.value)
def create_plot2(regular, super_fuel, diesel):
    plots = []
    
    if regular:
        df = read_csv_data('data/gasregularpormes.csv')
        monthly_averages = df.mean(axis=1, skipna=True)
        plots.append(hv.Curve(monthly_averages, label='Regular').opts(color='blue'))
        
    if super_fuel:
        df = read_csv_data('data/gassuperpormes.csv')
        monthly_averages = df.mean(axis=1, skipna=True)
        plots.append(hv.Curve(monthly_averages, label='Super').opts(color='green'))
        
    if diesel:
        df = read_csv_data('data/dieselpormes.csv')
        monthly_averages = df.mean(axis=1, skipna=True)
        plots.append(hv.Curve(monthly_averages, label='Diesel').opts(color='red'))
        
    if not plots:
        return hv.Curve([])  # Empty plot if none are selected
    
    overlay = hv.Overlay(plots).opts(width=800, xlabel='Mes', ylabel='Precio', title='Promedios mensuales')
    return overlay


# Options panel
options_panel = pn.WidgetBox(
    "# Opciones",
    regular_checkbox,
    super_checkbox,
    diesel_checkbox
)

# Bind the create_plot and create_plot2 functions to the checkbox widgets
bound_plot1 = pn.bind(create_plot, regular=regular_checkbox, super_fuel=super_checkbox, diesel=diesel_checkbox)
bound_plot2 = pn.bind(create_plot2, regular=regular_checkbox, super_fuel=super_checkbox, diesel=diesel_checkbox)

# Create two dynamic maps to update the plots based on the checkbox values
dynamic_plot1 = hv.DynamicMap(bound_plot1)
dynamic_plot2 = hv.DynamicMap(bound_plot2)

# Combine the two dynamic plots in a column layout
combined_plot = pn.Column(dynamic_plot1, dynamic_plot2)

# Create a Panel app with the options panel on the left and the combined plots on the right
app = pn.Row(options_panel, combined_plot)

# Show the app
app.show()
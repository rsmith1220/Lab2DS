import panel as pn
import pandas as pd
import hvplot.pandas
import holoviews as hv

# Data and labels
data = [25.49, 26.38, 22.26]
labels = ["Regular", "Super", "Diesel"]

# Read the CSV data
def read_csv_data(filepath):
    df = pd.read_csv(filepath, skipinitialspace=True)
    df = df.set_index(df.columns[0])
    df = df.drop(columns=["", "Promedio"])
    return df

# Calculate the average for each month
def calculate_monthly_averages(df):
    return df.mean(axis=1)

# Convert data to DataFrame for plotting
df = pd.DataFrame({
    'Tipo de gasolina': labels,
    'Amount': data
})

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

# Checkboxes for options panel
regular_checkbox = pn.widgets.Checkbox(name='Regular', value=True)
super_checkbox = pn.widgets.Checkbox(name='Super', value=True)
diesel_checkbox = pn.widgets.Checkbox(name='Diesel', value=True)

# Options panel
options_panel = pn.WidgetBox(
    "# Opciones",
    regular_checkbox,
    super_checkbox,
    diesel_checkbox
)

# Bind the create_plot function to the checkbox widgets
bound_plot = pn.bind(create_plot, regular=regular_checkbox, super_fuel=super_checkbox, diesel=diesel_checkbox)

# Create a dynamic map to update the plot based on the checkbox values
dynamic_plot = hv.DynamicMap(bound_plot)

# Create a Panel app with the options panel on the left and the plot on the right
app = pn.Row(options_panel, dynamic_plot)

# Show the app
app.show()

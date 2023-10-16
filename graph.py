import panel as pn
import pandas as pd
import hvplot.pandas

# Read the CSV file
df = pd.read_csv('data\dieselpormes.csv', skipinitialspace=True, index_col=0)

# Drop empty columns
df = df.dropna(axis=1, how='all')

# Create an interactive plot
plot = df.hvplot()

# Create a Panel app
app = pn.Column("# Monthly Data Visualization", plot)

# Show the app
app.show()

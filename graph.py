import panel as pn
import holoviews as hv
import pandas as pd

df_diesel = pd.read_csv('data/dieselpormes.csv')
df_regular = pd.read_csv('data/regularpormes.csv')
df_super = pd.read_csv('data/superpormes.csv')
df_super_aditivo = pd.read_csv('data/superconaditivo.csv')

def line_plot(df, año, title):
    data = df[df['Año'] == año]
    return hv.Curve(data, 'Mes', 'Precio', label=title).opts(line_width=2)

def histogram_promedio(df, title):
    precio_mean = df.groupby('Año')['Precio'].mean()
    return hv.Bars(precio_mean, 'Año', 'Precio', label=title)

def histogram_precio_mes(df, mes, title):
    data = df[df['Mes'] == mes]
    return hv.Bars(data, 'Año', 'Precio', label=title)

combustibles = {
    'Diesel': df_diesel,
    'Regular': df_regular,
    'Super': df_super,
    'Super con Aditivo': df_super_aditivo
}

def generate_plots(tipo_combustible, año, mes):
    df = combustibles[tipo_combustible]
    return (line_plot(df, año, f'Precio {tipo_combustible} {año}'),
            histogram_promedio(df, f'Precio Promedio General {tipo_combustible}'),
            histogram_precio_mes(df, mes, f'Precio {tipo_combustible} en {mes}'))

año_widget = pn.widgets.Select(name='Año', options=df_diesel['Año'].unique())
mes_widget = pn.widgets.Select(name='Mes', options=df_diesel['Mes'].unique())
tipo_combustible_widget = pn.widgets.Select(name='Tipo de Combustible', options=list(combustibles.keys()))

plots = pn.bind(generate_plots, tipo_combustible_widget, año_widget, mes_widget)

pn.Row(
    pn.WidgetBox(tipo_combustible_widget, año_widget, mes_widget),
    plots
).show()

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H3("Search Symbol"),
            dcc.Input(id='symbol-search', type='text', debounce=True),
            html.Div(id='symbol-dropdown'),
            html.Hr(),
            html.H4("Watchlist"),
            html.Div(id='watchlist')
        ], width=3),
        dbc.Col([
            dbc.Row([dbc.Col(dcc.Graph(id=f'chart-{i}'), width=4) for i in range(9)])
        ], width=9)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)






import pandas as pd
import gzip
import io

# Load the CSV file
with gzip.open('complete.csv.gz', 'rb') as f:
    df = pd.read_csv(io.BytesIO(f.read()))

# Create a dictionary for symbol to instrument key mapping
symbol_to_instrument_key = dict(zip(df['symbol'], df['instrument_key']))

# Example usage
symbol = 'RELIANCE'
instrument_key = symbol_to_instrument_key.get(symbol)
print(f"Instrument Key for {symbol}: {instrument_key}")



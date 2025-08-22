# # import dash
# # from dash import html, dcc, Input, Output
# # import requests
# # import plotly.graph_objs as go

# # app = dash.Dash(__name__)

# # watchlist = ['RELIANCE', 'TCS', 'HDFCBANK']  # Predefined for demo

# # app.layout = html.Div([
# #     html.H3("Symbol Watchlist"),
# #     html.Div([dcc.Graph(id=f"{sym}-tick") for sym in watchlist]),
# #     dcc.Interval(id="interval", interval=5000, n_intervals=0)
# # ])

# # @app.callback(
# #     [Output(f"{sym}-tick", "figure") for sym in watchlist],
# #     Input("interval", "n_intervals")
# # )
# # def update_charts(n):
# #     figures = []
# #     for sym in watchlist:
# #         r = requests.get(f"http://localhost:8000/chart/{sym}/1T")
# #         df = r.json()
# #         fig = go.Figure(go.Candlestick(
# #             x=[x["timestamp"] for x in df],
# #             open=[x["open"] for x in df],
# #             high=[x["high"] for x in df],
# #             low=[x["low"] for x in df],
# #             close=[x["close"] for x in df]
# #         ))
# #         fig.update_layout(title=sym)
# #         figures.append(fig)
# #     return figures

# # if __name__ == "__main__":
# #     app.run_server(debug=True)


# from flask import Flask, render_template, request, redirect, url_for
# from auth import UpstoxAuth
# from websocket_handler import WebSocketHandler

# from tick_store import TickStore
# from symbol_mapper import SymbolMapper
# import os

# app = Flask(__name__)

# # Load environment variables
# API_KEY = os.getenv("UPSTOX_API_KEY")
# API_SECRET = os.getenv("UPSTOX_API_SECRET")
# # REDIRECT_URI = os.getenv("UPSTOX_REDIRECT_URI")
# CSV_PATH = 'C://Users//Mahesh//Downloads//NSESymbolListCSV//NSE.csv'
# # Broker Configuration

# ######### OPEN ALGO TOTP KEY UD2PCQHXD4CUZDA6SIPT46ZTRHISEZS4
# # Market Data Configuration (Optional and Required only for XTS API Supported Brokers)

# #BROKER_API_KEY_MARKET = ''
# #BROKER_API_SECRET_MARKET = ''

# UPSTOX_REDIRECT_URI = 'http://127.0.0.1:5000/upstox/callback'  # Change if different

# CSV_PATH = 'C://Users//Mahesh//Downloads//NSESymbolListCSV//NSE.csv'
# print(CSV_PATH)
# print("----------------------------------------------------------------------------------------")
# symbol_mapper = SymbolMapper(CSV_PATH)
# tick_store = TickStore()

# auth = UpstoxAuth(API_KEY, API_SECRET, REDIRECT_URI)

# @app.route('/')
# def index():
#     return render_template('index.html', watchlist=tick_store.watchlist)

# @app.route('/auth')
# def auth_redirect():
#     auth_url = auth.get_authorization_url()
#     return redirect(auth_url)

# @app.route('/upstox/callback')
# def callback():
#     code = request.args.get('code')
#     tokens = auth.get_access_token(code)
#     access_token = tokens.get("access_token")

#     # Now that we have access token, initialize WebSocket
#     websocket_handler = WebSocketHandler(access_token, tick_store.watchlist)
#     websocket_handler.connect()

#     # return "Logged in successfully! You can now view real-time data."
#     return redirect(url_for('index'))

# @app.route('/add_to_watchlist', methods=['POST'])
# def add_to_watchlist():
#     symbol = request.form['symbol']
#     instrument_key = symbol_mapper.get_instrument_key(symbol)
#     if instrument_key:
#         tick_store.add_symbol(symbol, instrument_key)
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from auth import UpstoxAuth
from websocket_handler import WebSocketHandler
from symbol_mapper import SymbolMapper
from tick_store import TickStore
from candles import CandleGenerator
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Load environment variables
# API_KEY = os.getenv("UPSTOX_API_KEY")
# API_SECRET = os.getenv("UPSTOX_API_SECRET")
# REDIRECT_URI = os.getenv("UPSTOX_REDIRECT_URI")
# CSV_PATH = os.getenv("SYMBOL_CSV_PATH")

# CSV_PATH = os.getenv("SYMBOL_CSV_PATH")
CSV_PATH = 'C://Users//Mahesh//Downloads//NSESymbolListCSV//NSE.csv'
# Broker Configuration
API_KEY = ''
API_SECRET = '' 
REDIRECT_URI = 'http://127.0.0.1:5000/upstox/callback'  # Change if different

symbol_mapper = SymbolMapper(CSV_PATH)
tick_store = TickStore()

auth = UpstoxAuth(API_KEY, API_SECRET, REDIRECT_URI)

@app.route('/')
def index():
    # Render the main page
    return render_template('index.html', watchlist=tick_store.watchlist)

@app.route('/auth')
def auth_redirect():
    # Redirect to Upstox login
    auth_url = auth.get_authorization_url()
    return redirect(auth_url)

@app.route('/upstox/callback')
def callback():
    # After login, get the access token and connect WebSocket
    code = request.args.get('code')
    tokens = auth.get_access_token(code)
    print(tokens)
    access_token = tokens.get("access_token")

    websocket_handler = WebSocketHandler(access_token, tick_store.watchlist)
    websocket_handler.connect()

    # return "Logged in successfully! You can now view real-time data."

    return redirect(url_for('index'))

# @app.route('/add_to_watchlist', methods=['POST'])
# def add_to_watchlist():
#     # Add a symbol to the watchlist
#     symbol = request.form['symbol']
#     instrument_key = symbol_mapper.get_instrument_key(symbol)
#     if instrument_key:
#         tick_store.add_symbol(symbol, instrument_key)
#     return redirect(url_for('index'))

# @socketio.on('request_chart_update')
# def handle_chart_update(symbol):
#     # Handle real-time chart updates on WebSocket connection
#     instrument_key = symbol_mapper.get_instrument_key(symbol)
#     if instrument_key:
#         # Generate a candlestick chart
#         candle_generator = CandleGenerator(tick_store.ticks)
#         chart_html = candle_generator.generate_candles('1min')
        
#         # Send chart HTML to frontend
#         emit('update_chart', {'chart_html': chart_html})

@socketio.on('request_chart_update')
def handle_chart_update(symbol):
    print(" chart update io ---")
    instrument_key = symbol_mapper.get_instrument_key(symbol)
    if instrument_key:
        candle_generator = CandleGenerator(tick_store.ticks)
        chart_html = candle_generator.generate_candles('1min')
        emit(f'update_chart_{symbol}', {'chart_html': chart_html})


if __name__ == '__main__':
    socketio.run(app, debug=True)

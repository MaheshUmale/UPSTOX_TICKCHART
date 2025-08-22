from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import auth, websocket_handler, tick_store, candles, symbol_mapper
import uvicorn
import time
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# BROKER_API_KEY = os.getenv('BROKER_API_KEY')

# BROKER_API_SECRET = os.getenv('BROKER_API_SECRET')

# REDIRECT_URL = os.getenv('REDIRECT_URL')

API_KEY =  os.getenv('BROKER_API_KEY')
# "your_api_key"
API_SECRET = os.getenv('BROKER_API_SECRET')# "your_api_secret"
REDIRECT_URI = os.getenv('REDIRECT_URL') #"http://localhost"

symbol_map = symbol_mapper.load_symbol_mapping()
u = auth.login(API_KEY, API_SECRET, REDIRECT_URI)

def on_tick(tick):
    tick_data = {
        'timestamp': int(time.time() * 1000),
        'ltp': tick['last_traded_price']
    }
    symbol = tick['symbol']
    tick_store.store_tick(symbol, tick_data)

streamer = websocket_handler.UpstoxStreamer(u, on_tick)

@app.get("/watch/{symbol}")
def add_to_watch(symbol: str):
    instrument_key = symbol_map.get(symbol)
    streamer.start([instrument_key])
    return {"status": "watching", "instrument": instrument_key}

@app.get("/chart/{symbol}/{freq}")
def get_chart(symbol: str, freq: str):
    ticks = tick_store.get_ticks(symbol)
    chart = candles.generate_candles(ticks, freq)
    return chart.reset_index().to_dict(orient='records')

if __name__ == "__main__":
    uvicorn.run(app, port=8000)

# from collections import deque

# tick_buffer = {}

# def init_symbol(symbol):
#     if symbol not in tick_buffer:
#         tick_buffer[symbol] = deque(maxlen=10000)

# def store_tick(symbol, tick):
#     init_symbol(symbol)
#     tick_buffer[symbol].append(tick)

# def get_ticks(symbol):
#     return list(tick_buffer.get(symbol, []))

from collections import deque

class TickStore:
    def __init__(self):
        self.watchlist = []
        self.ticks = deque(maxlen=10000)

    def add_symbol(self, symbol, instrument_key):
        print(instrument_key)
        self.watchlist.append(instrument_key)

    def add_tick(self, tick_data):
        self.ticks.append(tick_data)

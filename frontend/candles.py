# # import pandas as pd
# # from datetime import datetime

# # def generate_candles(ticks, freq='1T'):
# #     df = pd.DataFrame(ticks)
# #     df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #     df.set_index('timestamp', inplace=True)
# #     candles = df['ltp'].resample(freq).ohlc()
# #     return candles.tail(20)  # recent 20

# import pandas as pd

# class CandleGenerator:
#     def __init__(self, tick_data):
#         self.tick_data = tick_data

#     def generate_candles(self, interval='1min'):
#         df = pd.DataFrame(self.tick_data)
#         df['timestamp'] = pd.to_datetime(df['timestamp'])
#         df.set_index('timestamp', inplace=True)
#         ohlc_dict = {
#             'price': ['ohlc'],
#             'quantity': ['sum'],
#             'timestamp': ['first']
#         }
#         ohlc_df = df.resample(interval).apply(ohlc_dict)
#         return ohlc_df


import plotly.graph_objs as go
import pandas as pd

class CandleGenerator:
    def __init__(self, tick_data):
        self.tick_data = tick_data

    def generate_candles(self, interval='1min'):
        df = pd.DataFrame(self.tick_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        # Resample data to generate OHLC (open, high, low, close)
        ohlc_data = df.resample(interval).agg({
            'price': ['first', 'max', 'min', 'last'],
            'quantity': 'sum'
        })

        # Create Plotly Candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc_data.index,
            open=ohlc_data['price']['first'],
            high=ohlc_data['price']['max'],
            low=ohlc_data['price']['min'],
            close=ohlc_data['price']['last']
        )])

        fig.update_layout(
            title="Candlestick Chart",
            xaxis_title="Time",
            yaxis_title="Price"
        )

        return fig.to_html(full_html=False)  # returns HTML for embedding in the webpage

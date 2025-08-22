

import upstox_client
import time
import collections
import pandas as pd

# Initialize a deque to store the last 10,000 ticks
tick_data = collections.deque(maxlen=10000)

def on_message(message):
    # Assuming message contains 'timestamp' and 'price'
    tick_data.append({'timestamp': message['timestamp'], 'price': message['price']})

    # Convert deque to DataFrame for processing
    df = pd.DataFrame(list(tick_data))

    # Generate 1-minute candlestick chart
    df_1min = df.resample('1T', on='timestamp').ohlc()

    # Generate 5-minute candlestick chart
    df_5min = df.resample('5T', on='timestamp').ohlc()

    # Update charts (implementation depends on your UI framework)
    update_charts(df, df_1min, df_5min)



# def on_message(message):
#     print(message)

def main():
    configuration = upstox_client.Configuration()
    access_token = 'YOUR_ACCESS_TOKEN'
    configuration.access_token = access_token

    streamer = upstox_client.MarketDataStreamerV3(
        upstox_client.ApiClient(configuration))

    def on_open():
        print("Connected. Subscribing to instrument keys.")
        streamer.subscribe(
            ["NSE_EQ|INE020B01018", "NSE_EQ|INE467B01029"], "full")

    streamer.on("open", on_open)
    streamer.on("message", on_message)
    streamer.connect()

if __name__ == "__main__":
    main()
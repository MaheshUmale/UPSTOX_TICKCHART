# from upstox_api.api import LiveFeedType
# from threading import Thread
# import time
# import upstox_client
# from upstox_client import 
# class UpstoxStreamer:
#     def __init__(self, upstox, on_tick):
#         self.u = upstox
#         self.on_tick = on_tick

#     def start(self, instrument_keys):
#         def run():
#             self.u.set_on_quote_update(self.on_tick)
#             self.u.subscribe(instrument_keys, LiveFeedType.Full)
#             while True:
#                 time.sleep(1)
#         Thread(target=run, daemon=True).start()
import time
import upstox_client
from collections import deque

class WebSocketHandler:
    def __init__(self, access_token, instrument_keys):
        print(access_token)
        print(instrument_keys)
        self.access_token = access_token
        self.instrument_keys = instrument_keys
        self.data_queue = deque(maxlen=10000)
        configuration = upstox_client.Configuration()
        
        configuration.access_token = self.access_token
        self.streamer = upstox_client.MarketDataStreamer(
            upstox_client.ApiClient(configuration)
        )

    def on_message(self, message):
        print("Message received:", message)
        self.data_queue.append(message)
        # Process message (e.g., update UI)

    def connect(self):
        print(" Connect WS--------------------------------self.access_token----->"+self.access_token)
        
        self.streamer.on("message", self.on_message)
        print(f"connect for  {self.instrument_keys}")
         # Assign callback functions to the streamer
        self.streamer.on_open = self.on_open
        self.streamer.on_message =self.on_message
        self.streamer.on_close = self.on_close
        self.streamer.on_error = self.on_error

        self.streamer.connect()
        time.sleep(3)
        



    # Define callback functions
    def on_open(self):
        print("Connection opened")
        # Subscribe to instruments after connection is established
        self.streamer.subscribe(self.instrument_keys, "full")

        # self.streamer.subscribe(["NSE_EQ|26009","NSE_EQ|INE062A01020","NSE_EQ|INE002A01018","NSE_EQ|INE062A01020","NSE_EQ|INE732I01013","NSE_EQ|INE062A01020","NSE_EQ|INE118H01025"], "full")  # Example: Subscribe to State Bank of Indi,"

  

    def on_close(self):
        print("Connection closed")

    def on_error(self,error):
        print("Error:", error)

       
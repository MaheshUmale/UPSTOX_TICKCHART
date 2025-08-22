# import upstox_client
# import time

# # Configure the Upstox client
# configuration = upstox_client.Configuration()

# # Replace with your access token

# # Initialize MarketDataStreamer
# streamer = upstox_client.MarketDataStreamer(
#     upstox_client.ApiClient(configuration)
# )

# # Define callback functions
# def on_open():
#     print("Connection opened")
#     # Subscribe to instruments after connection is established
#     streamer.subscribe(["NSE_EQ|26009"], "full")  # Example: Subscribe to State Bank of India

# def on_message(message):
#     print("Message received:", message)

# def on_close():
#     print("Connection closed")

# def on_error(error):
#     print("Error:", error)

# # Assign callback functions to the streamer
# streamer.on_open = on_open
# streamer.on_message = on_message
# streamer.on_close = on_close
# streamer.on_error = on_error

# print("# Connect to the streaming server")
# streamer.connect()

# # Keep the connection alive for some time (optional)
# time.sleep(10)

# print("# Subscribe to more instruments dynamically (optional)")
# streamer.subscribe(["NSE_EQ|11471"], "full")  # Example: Subscribe to Infosys

# time.sleep(10)

# # Disconnect from the streaming server
# streamer.disconnect()


import asyncio
import websockets
import ssl
import json
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Replace with your access token
access_token = ""
# 
api_version = '2.0'

# Configure OAuth2 access token for authorization
configuration = upstox_client.Configuration()
configuration.access_token = access_token

# Create an instance of the API client
api_client = upstox_client.ApiClient(configuration)
api_instance = upstox_client.WebsocketApi(api_client)

def get_market_data_feed_authorize(api_version, configuration):
    """Get authorization for market data feed."""
    api_instance = upstox_client.WebsocketApi(upstox_client.ApiClient(configuration))
    api_response = api_instance.get_market_data_feed_authorize(api_version)
    return api_response


async def connect_websocket():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    response = get_market_data_feed_authorize(api_version, configuration)
    
    async with websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context) as websocket:
        print("Connection established")

        # Subscribe to instrument(s)
        data = {
            "guid": "someguid",
            "method": "sub",
            "data": {
                "mode": "full",
                "instrument_keys": ["NSE_INDEX|Nifty 50"]
            }
        }
        await websocket.send(json.dumps(data))

        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=5)
                print(f"Received: {message}")
                # Process the received message as needed
            except asyncio.TimeoutError:
                print("Timeout occurred, checking connection...")
                try:
                    await websocket.send(json.dumps({"guid": "someguid", "method": "ping"}))
                    pong = await asyncio.wait_for(websocket.recv(), timeout=5)
                    if pong == '{"guid":"someguid","method":"pong"}':
                        print("Connection is alive")
                    else:
                        print("Connection is lost, reconnecting...")
                        break
                except:
                     print("Connection is lost, reconnecting...")
                     break
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed, reconnecting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break
async def main():
    while True:
        await connect_websocket()
        await asyncio.sleep(5)  # Wait for 5 seconds before attempting to reconnect

if __name__ == "__main__":
    asyncio.run(main())



# import upstox_client
# import configparser

# import upstox_client
# from upstox_client.rest import ApiException

# import webbrowser

# # def login(api_key, api_secret, redirect_uri):
# #     print(redirect_uri)
# #     session = Session(api_key)
# #     login_url = session.get_login_url(redirect_uri)
# #     webbrowser.open(login_url)
# #     code = input("Paste the code from URL after login: ").strip()
# #     session.set_code(code)
# #     access_token = session.retrieve_access_token(api_secret)
# #     return Upstox(api_key, access_token)

# # import webbrowser
# # import requests
# # from urllib.parse import urlencode, urlparse, parse_qs

# # API  key
# # 

# # API  secrete
# # 

# # redirect_uri
# # http://127.0.0.1:5000/upstox/callback

# from urllib.parse import urlencode


# BROKER_API_KEY = "
# BROKER_API_SECRET = ""
# REDIRECT_URI = "http://127.0.0.1:5000/upstox/callback"

# def login():
#     # Step 1: Generate Login URL
#     params = {
#         "client_id": BROKER_API_KEY,
#         "redirect_uri": REDIRECT_URI,
#         "response_type": "code",
#     }
#     auth_url = f"https://api.upstox.com/v2/login/authorization/dialog?{urlencode(params)}"

#     print(f"Opening login page... {auth_url}")
#     webbrowser.open(auth_url)

# # Step 2: User logs in and enters OTP manually on browser
# code = input("After login, paste the code from redirected URL here: ")

# # Step 3: Exchange code for access_token
# token_url = "https://api.upstox.com/v2/login/authorization/token"
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Accept": "application/json"
# }
# data = {
#     "code": code,
#     "client_id": BROKER_API_KEY,
#     "client_secret": BROKER_API_SECRET,
#     "redirect_uri": REDIRECT_URI,
#     "grant_type": "authorization_code"
# }

# response = requests.post(token_url, headers=headers, data=data)
# tokens = response.json()

# print("\n✅ Access Token:", tokens.get("access_token"))
# print("🔁 Refresh/Extended Token:", tokens.get("refresh_token"))




# # import http.client
# # import requests
# # import json
# # import os



# # def authenticate_broker(code):
# #     try:
# #         BROKER_API_KEY = os.getenv('BROKER_API_KEY')
# #         BROKER_API_SECRET = os.getenv('BROKER_API_SECRET')
# #         REDIRECT_URL = os.getenv('REDIRECT_URL')
# #         url = 'https://api.upstox.com/v2/login/authorization/token'
# #         data = {
# #             'code': code,
# #             'client_id': BROKER_API_KEY,
# #             'client_secret': BROKER_API_SECRET,
# #             'redirect_uri': REDIRECT_URL,
# #             'grant_type': 'authorization_code',
# #         }
# #         response = requests.post(url, data=data)

# #         if response.status_code == 200:
# #             response_data = response.json()
# #             if 'access_token' in response_data:
# #                 return response_data['access_token'], None
# #             else:
# #                 return None, "Authentication succeeded but no access token was returned. Please check the response."
# #         else:
# #             # Parsing the error message from the API response
# #             error_detail = response.json()  # Assuming the error is in JSON format
# #             error_messages = error_detail.get('errors', [])
# #             detailed_error_message = "; ".join([error['message'] for error in error_messages])
# #             return None, f"API error: {error_messages}" if detailed_error_message else "Authentication failed. Please try again."
# #     except Exception as e:
# #         return None, f"An exception occurred: {str(e)}"


import webbrowser
import requests
from urllib.parse import urlencode

class UpstoxAuth:
    def __init__(self, api_key, api_secret, redirect_uri):
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self):
        params = {
            "client_id": self.api_key,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
        }
        auth_url = f"https://api.upstox.com/v2/login/authorization/dialog?{urlencode(params)}"
        return auth_url

    def get_access_token(self, code):
        token_url = "https://api.upstox.com/v2/login/authorization/token"
        data = {
            "code": code,
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        response = requests.post(token_url, data=data)
        return response.json()

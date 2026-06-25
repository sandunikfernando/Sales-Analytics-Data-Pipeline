import requests
import json
import os

API_URL = os.getenv("API_URL")
response = requests.get(API_URL)
data = response.json()
print(json.dumps(data["carts"][0], indent=4))
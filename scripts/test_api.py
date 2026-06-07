# import requests

# url = "https://dummyjson.com/carts"

# response = requests.get(url)
# print(response.status_code)
# data = response.json()
# print(data.keys())



import requests
import json

response = requests.get("https://dummyjson.com/carts")
data = response.json()
print(json.dumps(data["carts"][0], indent=4))
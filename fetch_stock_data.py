import http.client
import json

conn = http.client.HTTPSConnection("stock.indianapi.in")

headers = { 'X-Api-Key': "sk-live-6snQG47cECsrtyFWYHSmuGVsBRPP3r51QZS3NSgQ" }

conn.request("GET", "/stock?name=Eternal", headers=headers)

res = conn.getresponse()
data = res.read()

# Parse the JSON data
json_data = json.loads(data.decode("utf-8"))

# Save to a JSON file with proper formatting
with open('stock_data.json', 'w') as f:
    json.dump(json_data, f, indent=4)

print("Data has been saved to stock_data.json")
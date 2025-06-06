import requests

url = 'https://api.upstox.com/v3/historical-candle/intraday/NSE_EQ%7CINE848E01016/minutes/1'
headers = {
    'Accept': 'application/json'
}

response = requests.get(url, headers=headers)

# Check the response status
if response.status_code == 200:
    # Do something with the response data (e.g., print it)
    print(response.json())
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")

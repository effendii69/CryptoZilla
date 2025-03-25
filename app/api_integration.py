import requests

ALPHA_VANTAGE_API_KEY = 'WN9MPRWNQUMCVS6C'

def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if "Global Quote" in data:
        return data["Global Quote"]
    else:
        return {"Error": "Invalid Symbol or API limit reached"}

import os
import requests, json
ENDPOINT_URL ="https://paper-api.alpaca.markets"
API_KEY = "PKQ6JRI1NRLNKECCEJ86"
SECRET_KEY = "VYxbJVGezVU7LZRa4bx1lGkWZ4klOIJQQV2IQ2uz"


ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT_URL)
ORDER_URL = '{}/v2/orders'.format(ENDPOINT_URL)
DATA_URL = 'https://data.alpaca.markets/v1'
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

# os.environ["SECRET_KEY"]
# account = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ENDPOINT_URL, api_version='v2')

# everything below here is REST
def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


# returns an ID for the order submitted
def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDER_URL, json=data, headers=HEADERS)
    return json.loads(r.content)


def get_orders():
    print("searching for orders")
    r = requests.get(ORDER_URL, headers=HEADERS)
    return json.loads(r.content)
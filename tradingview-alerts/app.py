import requests, json
from chalice import Chalice, Rate
import os

ENDPOINT_URL = "https://paper-api.alpaca.markets"

ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT_URL)
ORDER_URL = '{}/v2/orders'.format(ENDPOINT_URL)
CLOCK_URL = '{}/v2/clock'.format(ENDPOINT_URL)
DATA_URL = 'https://data.alpaca.markets/v1'
HEADERS = {'APCA-API-KEY-ID': os.environ['API_KEY'], 'APCA-API-SECRET-KEY': os.environ['SECRET_KEY']}

app = Chalice(app_name='luna6trade')


# print(os.environ['API_KEY'])

def get_alpaca_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


print(get_alpaca_account())


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


@app.route('/')
def index():
    return {"made by alexander lin": "luna6algotrader",
            "message": "this is technically an api, and by visiting the URL i think you're calling on a lambda function..."
                       "anyways, im trying to make this webpage or api prettier but I'll get to it after the trading logic",
            "cheers": "thanks for visiting! (:"}


@app.route('/account', methods=['POST'])
def get_account():
    request = app.current_request
    webhook_message = request.json_body

    return {
        "account_id": get_alpaca_account()["id"],
        "message": webhook_message
    }


@app.schedule(Rate(1, unit=Rate.HOURS))
def every_min(event):
    r = requests.get(CLOCK_URL, headers=HEADERS)
    marketclock = json.loads(r.content)

    if marketclock["is_open"]:
        # trading logic
        create_order("MSFT", 1, "buy", "market", "gtc")

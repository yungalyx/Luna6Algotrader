import requests, json
from chalice import Chalice, Rate
import os

ENDPOINT_URL = "https://paper-api.alpaca.markets"

ACCOUNT_URL = '{}/v2/account'.format(ENDPOINT_URL)
ORDER_URL = '{}/v2/orders'.format(ENDPOINT_URL)
CLOCK_URL = '{}/v2/clock'.format(ENDPOINT_URL)
DATA_URL = 'https://data.alpaca.markets/v1'
HEADERS = {'APCA-API-KEY-ID': os.environ['API_KEY'], 'APCA-API-SECRET-KEY': os.environ['SECRET_KEY']}
FINNHUBHEADER = {'X-Finnhub-Token': os.environ['FINNHUBKEY']}

app = Chalice(app_name='luna6trade')


def test1():
    stonks = ['AAPL', 'RACE', 'TSLA', 'QQQ']
    for ticker in stonks:
        r = requests.get('https://finnhub.io/api/v1/quote?symbol={}'.format(ticker), headers=FINNHUBHEADER)  # or header
        print(r.json())


def get_alpaca_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


print(get_alpaca_account())

#

def create_bracket_order(symbol, qty, side, type, limit, stop):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": 'day',
        'order_class':'bracket',
        'take_profit': {
            'limit_price': limit
        },
        'stop_loss': {
            'stop_price': stop
        }
    }
    r = requests.post(ORDER_URL, json=data, headers=HEADERS)
    return json.loads(r.content)




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
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=AAPL', headers=FINNHUBHEADER)
        current_price = quote.json()
        curr = (current_price['c'])

        target = requests.get('https://finnhub.io/api/v1/stock/price-target?symbol=AAPL', headers=FINNHUBHEADER)
        target_price = target.json()
        shouldbe = (target_price['targetHigh'] + target_price['targetMedian'])/2

        # STOP LOSS 5% below and Take profit 5% above
        if shouldbe > curr:
            create_bracket_order('AAPL', 1, 'buy', 'market', limit=shouldbe, stop=curr*0.93)

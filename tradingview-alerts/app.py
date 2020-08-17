from chalice import Chalice, Rate
from alpacatrade import *


app = Chalice(app_name='tradingview-alerts')
print(get_account()["id"])
print(create_order("TQQQ", 1, "buy", "market", "gtc"))


@app.route('/')
def index():
    return {"tradingview-alerts": "luna6algotrader"}


@app.route('/execute', methods=['POST'])
def execute_order():
    request = app.current_request
    webhook_message = request.json_body

    return {
        "message": webhook_message
    }


@app.route('/history')
def history():
    log = [
        {"trade 1": "bought 3 nikes"},
        {"trade 2": "sold 5 tqqq"}
    ]
    return {"log": log}


@app.schedule(Rate(30, unit=Rate.MINUTES))
def every_thirty_min(event):
    create_order("AAPL", 1, "buy", "market", "gtc")





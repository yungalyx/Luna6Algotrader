from chalice import Chalice

app = Chalice(app_name='tradingview-alerts')


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

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

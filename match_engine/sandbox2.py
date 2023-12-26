import requests
import json
import random
import time
import multiprocessing

def post_request(url_endpoint, action, payload, token=None):
    header = {'Content-Type': "application/json"}
    if token:
        header['Authorization'] = f"Token {token}"

    content = None

    if action == "POST":
        content = requests.post(url=url_endpoint, data=json.dumps(payload), headers=header)
    elif action == "GET":
        content = requests.post(url=url_endpoint, headers=header)
    return content

# token = "911f830493fb7bb3bb65541218f64a6f598f8532"  # account1
token = "250c1000a7b0f0c3f2ec3a7fd2904249d13cf872"  # account2
# token = "d4dc42e259710a88d906bfd961c61f58098a08ca"  # account3
# token = "8c83d4aa4445f5d66e23fe0a74310a79631c47e0"  # account4

url_endpoint = "http://127.0.0.1:8000/api/order/"

def send_func():
    n = 100000
    for _ in range(n):
        payload = {
            "symbol": "AAPL",
            "order_type": "LMT",
            "instruction": "BUY",
            # "quantity": 1,
            "quantity": random.randint(1, 100),
            "price": random.randint(100, 10000) / 100
        }
        try:
            start = time.time()
            res = post_request(url_endpoint, "POST", payload, token)
            end = time.time()
            print(res, end - start)
        except Exception as e:
            print(e)


def publish_func():
    from amqp import AMQP
    amqp = AMQP()
    connection = amqp.connection

    exchange_name = f"orderbook_a"
    routing_key = f"exchange.orderbook.a"

    n = 100000
    payload = {}
    for _ in range(n):
        payload = {
            'order': {
                'user_securities_account_id': 5,
                'symbol': "AAPL",
                'order_type': "LMT",
                'order_id': 2000000 + n,
                'instruction': "BUY",
                'quantity': random.randint(1,100),
                'price': 100 + (random.randint(100, 10000) / 100)
            }
        }
        channel = amqp.channel
        channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(payload))

if __name__ == "__main__":
    n = 12
    for i in range(n):
        worker = multiprocessing.Process(target=send_func)
        worker.start()

    # n = 4
    # for i in range(n):
    #     worker = multiprocessing.Process(target=publish_func)
    #     worker.start()
    # # publish_func()
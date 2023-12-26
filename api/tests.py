from django.test import TestCase

# Create your tests here.

import requests
import json


def post_request(url_endpoint, action, payload):
    header = {
        # 'Authorization': f"Bearer {token}",
        'Content-Type': "application/json"
    }
    content = None
    if action == "POST":
        content = requests.post(url=url_endpoint, data=json.dumps(payload), headers=header)
    elif action == "GET":
        content = requests.post(url=url_endpoint, headers=header)
    return content


url_endpoint = "http://localhost:8000/api/trade/"
# {'timestamp': 1650596928675141, 'incoming_order_id': 13, 'book_order_id': 11, 'instruction': 'SELL', 'quantity': 7, 'price': 23.0, 'symbol': 'AAAA'}
payload = {
    "incoming_order_id": 13,
    "book_order_id": 11,
    "symbol": "AAAA",
    "instruction": "SELL",
    "quantity": 7,
    "price": 23,
    "timestamp": 1650596928675141
}
res = post_request(url_endpoint, "POST", payload)
print(res)
print(res.__dict__)

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parents[1]

from amqp import AMQP
from signals import WorkerQueue
import time, datetime
import requests
import json
import multiprocessing
import sys

# amqp = AMQP()
# channel = amqp.channel

class MyQuoteWorker(WorkerQueue):
    def __init__(self, worker_name, queue_name, *args, **kwargs):
        super().__init__(worker_name, queue_name, *args, **kwargs)
        self.url_endpoint = "http://127.0.0.1:8000/api/quote/"

    def preset_worker(self, *args, **kwargs):
        """ Runs once
        """

    def process_task(self, *args, **kwargs):
        """
            Default method:
            >> self.process_task(routing_key=method.routing_key, body=decoded_body)

            use kwargs.get('routing_key') and kwargs.get('body') to get values.

            >> decoded_body = kwargs.get('body', [])
            decoded body should be list format for the v2 batch trades

            decoded_body = [{
                incoming_order_id: int,
                book_order_id: int,
                symbol: str max 5 characters,
                instruction: "BUY" or "SELL",
                quantity: int,
                price: float,
                timestamp: int,
            }, ...]
        """
        start = time.time()
        print(f"{datetime.datetime.now()} [{self.worker_name}] {kwargs.get('routing_key', '')} : {kwargs.get('body', '')}")
        decoded_body = kwargs.get('body', {})

        def post_request(url_endpoint, action, payload):
            token = "f31dd6d0a570d1fd88fba79bc43c9fe5061d674e"
            header = {
                'Authorization': f"Token {token}",
                'Content-Type': "application/json"
            }
            content = None
            if action == "POST":
                content = requests.post(url=url_endpoint, data=json.dumps(payload), headers=header)
            elif action == "GET":
                content = requests.post(url=url_endpoint, headers=header)
            return content

        payload = {
            "symbol": decoded_body["symbol"],
            "quote": decoded_body["quote"],
        }
        res = post_request(self.url_endpoint, "POST", payload)
        end = time.time()
        print(f"\t {self.worker_name} {res} {round(end - start, 4)}")
        return

class Counter:
    id = 0
    def __init__(self):
        self.id = Counter.id
        Counter.id += 1

def thread_worker(id):
    print(f"setting up worker {id}")
    queue_name = "confirm_quote"
    tw1 = MyQuoteWorker(f"worker_{id}", queue_name).worker()


if __name__ == "__main__":
    worker_count = 8
    for i in range(worker_count):
        worker = multiprocessing.Process(target=thread_worker, args=(i,))
        worker.start()




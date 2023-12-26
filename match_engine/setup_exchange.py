from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parents[1]

import pika
import sys
import os
import json
import datetime
import time
import pickle
import io
import logging

from engine import OrderBook, OrderInstruction, LimitOrder, MarketOrder, CancelOrder
from signals import ExchangeWorker, TimeLogger

from google.cloud import storage
sa_key = os.environ.get('SERVICE_ACCOUNT_FILE')
gcs_client = storage.Client.from_service_account_json(os.path.join(BASE_DIR, sa_key))
bucket_name = os.environ.get('GCS_BUCKET')
gcs_bucket = gcs_client.get_bucket(bucket_name)

"""
    Placing orders
    payload = {
        'order': {
            'symbol': 'AAAA',
            'order_type': 'LMT',        # ['LMT', 'MKT', 'CNL']
            'order_id': 1,
            'instruction': 'BUY',       # ['BUY', 'SELL']
            'quantity': 10,
            'price': 20.50
        }
    }

    Getting exchange data
    payload = {
        'exchange': {
            'symbol': 'AAAA'
        }
    }

"""


class MyExchangeWorker(ExchangeWorker):
    def __init__(self, exchange_name, routing_key, *args, **kwargs):
        super().__init__(exchange_name, routing_key, *args, **kwargs)
        self.orderbook_symbols = {}
        self.timelogger = TimeLogger(60)


    def preset_worker(self, *args, **kwargs):
        """ Runs once
        """
        pass

        # symbol = "TEST1"
        # self.orderbook_symbols[symbol] = OrderBook(symbol, amqp=self.amqp, confirm_execution=True)
        # print(f" Starting exchange orderbooks: {list(self.orderbook_symbols.keys())}")

    def process_task(self, *args, **kwargs):
        """
            Default method:
            >> self.process_task(routing_key=method.routing_key, body=decoded_body)

            use kwargs.get('routing_key') and kwargs.get('body') to get values.
        """

        # print(f" [x] {kwargs.get('routing_key', '')} : {kwargs.get('body', '')}")
        decoded_body = kwargs.get('body', None)
        order = decoded_body.get('order', None)
        exchange = decoded_body.get('exchange', None)
        heartbeat = decoded_body.get('heartbeat', None)

        if exchange:
            symbol = exchange['symbol']
            # TODO: add system to store exchange data, save into google cloud

            # pickle object
            # setup service google cloud storage
            # write i/o save to storage bucket

            OB = self.orderbook_symbols[symbol]
            timestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"OB_{symbol}_{timestr}.txt"

            lines = OB.get_bid_ask_lines()
            output = io.StringIO()
            for line in lines:
                output.write(line+"\n")
            blob = gcs_bucket.blob(f"orderbook/{filename}")
            output.seek(0)
            blob.upload_from_file(output)
            output.close()
            print(f"EXCHANGE DATA SAVED: orderbook/{filename}")
            return

        if order:
            symbol = order['symbol']
            if symbol not in self.orderbook_symbols:
                self.orderbook_symbols[symbol] = OrderBook(symbol, amqp=self.amqp, confirm_execution=True)
            OB = self.orderbook_symbols[symbol]

            def execute_order(order):
                if order['order_type'] == 'CNL':
                    OB.process_order(CancelOrder(order['order_id']))
                    return

                instruction = {'BUY': OrderInstruction(1), 'SELL': OrderInstruction(0)}
                if order['order_type'] == 'LMT':
                    OB.process_order(LimitOrder(
                        order['user_securities_account_id'],
                        order['order_id'],
                        order['symbol'],
                        instruction[order['instruction']],
                        order['quantity'],
                        order['price']
                    ))
                elif order['order_type'] == 'MKT':
                    OB.process_order(MarketOrder(
                        order['user_securities_account_id'],
                        order['order_id'],
                        order['symbol'],
                        instruction[order['instruction']],
                        order['quantity'],
                    ))
                return

            # print(f"{datetime.datetime.now()} Received {order['order_type']}")
            execute_order(order)
            # OB.batch_interval_payload(1)  # in seconds, this step is done inside of OB.process_order method
            if self.timelogger.validate_time():
                print(f"Active OB: {self.orderbook_symbols.keys()}")
                for k in self.orderbook_symbols:
                    print(self.orderbook_symbols[k])
                    print("\n \n \n")
            return

        if heartbeat:
            symbol = heartbeat['symbol']
            if symbol in self.orderbook_symbols:
                OB = self.orderbook_symbols[symbol]
                OB.batch_interval_payload(1)  # in seconds

        print(f" [Incorrect Message] {kwargs.get('routing_key', '')} : {kwargs.get('body', '')}")
        return


def main():
    exchange_name = "orderbook_a"
    routing_key = "exchange.orderbook.a"
    MyExchangeWorker(exchange_name, routing_key).worker()


if __name__ == '__main__':
    main()
    # print(MyExchangeWorker("a", "a").__dict__)

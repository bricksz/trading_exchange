from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parents[1]

from time import time

from sortedcontainers import SortedList
from order import Order, OrderInstruction, MarketOrder, LimitOrder, CancelOrder
from trade import Trade
import pika
import json
import sys
import datetime

class OrderBook:
    def __init__(self, symbol, amqp=None, confirm_execution=False):
        self.ts = datetime.datetime.now()
        self.symbol = symbol
        self.bids: SortedList[Order] = SortedList()
        self.asks: SortedList[Order] = SortedList()
        self.trades = []

        self.amqp = amqp
        self.confirm_execution = confirm_execution
        self.confirm_execution_queue_name = "confirm_execution"
        self.confirm_quote_queue_name = "confirm_quote"

        self.confirm_interval = 1       # seconds
        self.batch_trades = []
        self.trades_index = 0

    def process_order(self, incoming_order):

        def continue_order():
            """ custom while clause trigger
            """
            if incoming_order.instruction == OrderInstruction.BUY:
                if incoming_order.__class__ == LimitOrder:
                    return len(self.asks) > 0 and incoming_order.price >= self.asks[0].price    # Limit Order BUY side
                elif incoming_order.__class__ == MarketOrder:
                    return len(self.asks) > 0                                                   # Market Order BUY side
            else:
                if incoming_order.__class__ == LimitOrder:
                    return len(self.bids) > 0 and incoming_order.price <= self.bids[0].price    # Limit Order SELL side
                elif incoming_order.__class__ == MarketOrder:
                    return len(self.bids) > 0                                                   # Market Order SELL side

        if incoming_order.__class__ == CancelOrder:
            for order in self.bids:
                if incoming_order.order_id == order.order_id:
                    self.bids.discard(order)
                    break
            for order in self.asks:
                if incoming_order.order_id == order.order_id:
                    self.asks.discard(order)
                    break
            return

        while continue_order():
            book_order = None               # Order class object
            if incoming_order.instruction == OrderInstruction.BUY:
                book_order = self.asks.pop(0)
            else:
                book_order = self.bids.pop(0)

            # For the same volume order between incoming and book order
            if incoming_order.remainder_fill_quantity == book_order.remainder_fill_quantity:
                volume = incoming_order.remainder_fill_quantity
                incoming_order.remainder_fill_quantity -= volume
                book_order.remainder_fill_quantity -= volume
                trade = Trade(
                    instruction=incoming_order.instruction,
                    symbol=incoming_order.symbol,
                    quantity=volume,
                    price=book_order.price,
                    incoming_order_id=incoming_order.order_id,
                    book_order_id=book_order.order_id
                )
                # self.confirm_trade(trade.get_payload())
                # self.trades.append(trade)
                # self.confirm_quote({"symbol": incoming_order.symbol, "quote": book_order.price})  # moved to batch_interval_payload

                # TODO: batches
                self.batch_trades.append(trade.get_payload())
                self.batch_interval_payload(self.confirm_interval)  # in seconds
                break

            # Incoming order has greater volume than book order
            elif incoming_order.remainder_fill_quantity > book_order.remainder_fill_quantity:
                volume = book_order.remainder_fill_quantity
                incoming_order.remainder_fill_quantity -= volume
                book_order.remainder_fill_quantity -= volume
                trade = Trade(
                    instruction=incoming_order.instruction,
                    symbol=incoming_order.symbol,
                    quantity=volume,
                    price=book_order.price,
                    incoming_order_id=incoming_order.order_id,
                    book_order_id=book_order.order_id
                )
                # self.confirm_trade(trade.get_payload())
                # self.trades.append(trade)
                # self.confirm_quote({"symbol": incoming_order.symbol, "quote": book_order.price})    # moved to batch_interval_payload

                # TODO: batches
                self.batch_trades.append(trade.get_payload())
                self.batch_interval_payload(self.confirm_interval)  # in seconds

            # Book order has greater volume than incoming order
            elif incoming_order.remainder_fill_quantity < book_order.remainder_fill_quantity:
                volume = incoming_order.remainder_fill_quantity
                incoming_order.remainder_fill_quantity -= volume
                book_order.remainder_fill_quantity -= volume
                trade = Trade(
                    instruction=incoming_order.instruction,
                    symbol=incoming_order.symbol,
                    quantity=volume,
                    price=book_order.price,
                    incoming_order_id=incoming_order.order_id,
                    book_order_id=book_order.order_id,
                )
                # self.confirm_trade(trade.get_payload())
                # self.trades.append(trade)
                # self.confirm_quote({"symbol": incoming_order.symbol, "quote": book_order.price})    # moved to batch_interval_payload

                # TODO: batches
                self.batch_trades.append(trade.get_payload())
                self.batch_interval_payload(self.confirm_interval)  # in seconds

                if book_order.instruction == OrderInstruction.SELL:
                    self.asks.add(book_order)
                else:
                    self.bids.add(book_order)
                break

        if incoming_order.remainder_fill_quantity > 0 and incoming_order.__class__ == LimitOrder:
            if incoming_order.instruction == OrderInstruction.BUY:
                self.bids.add(incoming_order)
            else:
                self.asks.add(incoming_order)

        if incoming_order.remainder_fill_quantity > 0 and incoming_order.__class__ == MarketOrder:
            volume = incoming_order.remainder_fill_quantity
            trade = Trade(
                instruction=incoming_order.instruction,
                symbol=incoming_order.symbol,
                quantity=0,
                price=0.0,
                incoming_order_id=incoming_order.order_id,
                book_order_id=-1
            )
            # self.confirm_trade(trade.get_payload())
            # self.trades.append(trade)
            # self.confirm_quote({"symbol": incoming_order.symbol, "quote": 0.0})     # moved to batch_interval_payload

            # TODO: batches
            self.batch_trades.append(trade.get_payload())
            self.batch_interval_payload(self.confirm_interval)        # in seconds

    def batch_interval_payload(self, interval):
        ts_now = datetime.datetime.now()
        if (self.ts < ts_now) or len(self.batch_trades) > 5000:
            self.ts = ts_now + datetime.timedelta(seconds=interval)
            if len(self.batch_trades) > 0:
                last_trade = self.batch_trades[-1]
                self.confirm_trade(self.batch_trades)
                self.confirm_quote({
                    "symbol": last_trade["symbol"],
                    "quote": last_trade["price"],
                })
                self.trades.extend(self.batch_trades)
                self.batch_trades = []
        return

    def confirm_trade(self, payload):
        if self.amqp and self.confirm_execution:
            if not self.amqp.connection_status():
                print("AMQP CONNECTION LOST! RECONNECTING.....")
                self.amqp.reconnect()
            channel = self.amqp.channel
            channel.queue_declare(queue=self.confirm_execution_queue_name, durable=True)
            channel.basic_publish(
                exchange='', routing_key=self.confirm_execution_queue_name, body=json.dumps(payload),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )
            print(f"\t\t {datetime.datetime.now()} Trade Executions: {len(payload)}")

    def confirm_quote(self, payload):
        if self.amqp and self.confirm_execution:
            if not self.amqp.connection_status():
                print("AMQP CONNECTION LOST! RECONNECTING.....")
                self.amqp.reconnect()
            channel = self.amqp.channel
            channel.queue_declare(queue=self.confirm_quote_queue_name, durable=True)
            channel.basic_publish(
                exchange='', routing_key=self.confirm_quote_queue_name, body=json.dumps(payload),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )

    def get_bid(self):
        return self.bids[0].price if len(self.bids) > 0 else None

    def get_ask(self):
        return self.asks[0].price if len(self.asks) > 0 else None

    def get_bid_ask_lines(self):
        lines = []
        lines.append("-" * 5 + "OrderBook_" + str(self.symbol) + "-" * 5)
        lines.append("\nAsks:")
        asks = self.asks.copy()[:250]
        while len(asks) > 0:
            lines.append(str(asks.pop()))
        lines.append("\t" * 3 + "Bids:")
        bids = list(reversed(self.bids.copy()))[:250]
        while len(bids) > 0:
            lines.append("\t" * 3 + str(bids.pop()))
        lines.append("-" * 20)
        return lines

    def populate_dummy_trades(self):
        # from random import getrandbits, randint
        #
        # instruction = {'BUY': OrderInstruction(1), 'SELL': OrderInstruction(0)}
        # orders = []
        # order_id_offset = 1000000000
        # n = 1000
        # for i in range(n):
        #     if bool(getrandbits(1)):
        #         orders.append(LimitOrder(2, order_id_offset+i, 'AAPL', instruction['BUY'], randint(1, 200), randint(100, 10000) / 100))
        #     else:
        #         orders.append(LimitOrder(1, order_id_offset+i, 'AAPL', instruction['SELL'], randint(1, 200), randint(100, 10000) / 100))
        # start = time()
        # for order in orders:
        #     self.process_order(order)
        # end = time()
        # total_time = (end - start)
        # print("Time: " + str(total_time))
        # print("Time per order (us): " + str(1000000 * total_time / n))
        # print("Orders per second: " + str(n / total_time))
        pass

    def __repr__(self):
        lines = self.get_bid_ask_lines()
        return "\n".join(lines)

    def __len__(self):
        return len(self.asks) + len(self.bids)



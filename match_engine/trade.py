from time import time
from order import OrderInstruction


class Trade(object):
    def __init__(
            self,
            instruction: OrderInstruction,
            symbol: str,
            quantity: int,
            price: float,
            incoming_order_id: int,
            book_order_id: int
    ):
        self.timestamp = int(time()*1e6)    # unix timestamp in microseconds, 16 digits
        self.incoming_order_id = incoming_order_id
        self.book_order_id = book_order_id
        self.instruction = instruction
        self.quantity = quantity
        self.price = price
        self.symbol = symbol

    def __repr__(self):
        return f"Executed: {self.instruction} {self.quantity} Shares at {self.price}"

    def get_payload(self):
        payload = {
            "timestamp": self.timestamp,
            "incoming_order_id": self.incoming_order_id,
            "book_order_id": self.book_order_id,
            "instruction": "BUY" if self.instruction == OrderInstruction.BUY else "SELL",
            "quantity": self.quantity,
            "price": self.price,
            "symbol": self.symbol,
        }
        return payload

if __name__ == "__main__":
    pass
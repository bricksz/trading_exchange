from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

from enum import Enum
from time import time


class OrderInstruction(Enum):
    SELL = 0
    BUY = 1


class OrderType(Enum):
    MARKET = 0
    LIMIT = 1


class Order:
    def __init__(
            self,
            user_securities_account_id: int,
            order_id: int,
            symbol: str,
            instruction: OrderInstruction,
            quantity: int
    ):
        self.user_securities_account_id = user_securities_account_id        # int
        self.order_id = order_id                    # int
        self.symbol = symbol                        # str
        self.timestamp = int(time()*1e6)            # unix timestamp in microseconds, 16 digits
        self.instruction = instruction              # see enum class OrderInstruction
        self.quantity = quantity                    # int
        self.remainder_fill_quantity = quantity     # int


class CancelOrder:
    def __init__(self, order_id: int):
        self.order_id = order_id

    def __repr__(self):
        return f"Cancel Order: {self.order_id}"


class MarketOrder(Order):
    def __init__(
            self,
            user_securities_account_id: int,
            order_id: int,
            symbol: str,
            instruction: OrderInstruction,
            quantity: int
    ):
        super().__init__(user_securities_account_id, order_id, symbol, instruction, quantity)
        self.user_securities_account_id = user_securities_account_id

    def __repr__(self):
        side = "BUY" if self.instruction == OrderInstruction(1) else "SELL"
        return f"Market Order: {side} {self.symbol} " \
               f"{self.quantity} " \
               f"(Filled: {self.quantity-self.remainder_fill_quantity}) " \
               f"Shares " \
               f"\t\t (order_id: {self.order_id}, usa_id: {self.user_securities_account_id})"


class LimitOrder(MarketOrder):
    def __init__(
            self,
            user_securities_account_id: int,
            order_id: int,
            symbol: str,
            instruction: OrderInstruction,
            quantity: int,
            price: float
    ):
        super().__init__(user_securities_account_id, order_id, symbol, instruction, quantity)
        self.price = price

    # Custom less than used in SortedList class to sort the array of LimitOrder
    def __lt__(self, other):
        if self.price != other.price:
            if self.instruction == OrderInstruction.BUY:
                return self.price > other.price
            else:
                return self.price < other.price
        elif self.timestamp != other.timestamp:
            return self.timestamp < other.timestamp
        elif self.quantity != other.quantity:
            return self.quantity < other.quantity

    def __repr__(self):
        side = "BUY" if self.instruction == OrderInstruction(1) else "SELL"
        return f"Limit Order: {side} {self.symbol} " \
               f"{self.quantity} " \
               f"(Filled: {self.quantity-self.remainder_fill_quantity}) " \
               f"Shares at {self.price:0.2f} " \
               f"\t\t (order_id: {self.order_id}, usa_id: {self.user_securities_account_id})"

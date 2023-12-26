from signals import TradeWorker, TradeQueue


if __name__ == "__main__":
    queue_name = "confirm_execution"
    tq = TradeQueue(queue_name)
    for n in range(20):
        payload = {"msg": f"trade executed id: {n}"}
        tq.confirm(payload)
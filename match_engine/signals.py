from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parents[1]

from amqp import AMQP
import pika
import json
import time
import datetime
import traceback

def override(func):
    """ Indicates class methods meant to be rewritten """
    return func


class TimeLogger:
    def __init__(self, interval):
        self.interval = interval
        self.next_timestamp = datetime.datetime.today() + datetime.timedelta(seconds=self.interval)

    def increment_next_timestamp(self):
        self.next_timestamp = datetime.datetime.today() + datetime.timedelta(seconds=self.interval)

    def validate_time(self):
        time_now = datetime.datetime.today()
        if time_now >= self.next_timestamp:
            self.increment_next_timestamp()
            return True
        return False


class Worker:
    def __init__(self, *args, **kwargs):
        self.amqp = AMQP()
        self.connection = self.amqp.connection
        self.channel = self.amqp.channel

    @override
    def process_task(self, *args, **kwargs):
        pass

    @override
    def preset_worker(self, *args, **kwargs):
        pass

# Dont use this with ExchangeWorker
class TradeQueue(Worker):
    def __init__(self, queue_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, durable=True)

    def confirm(self, payload):
        if not self.amqp.connection_status():
            self.amqp.reconnect()
        self.channel.basic_publish(
            exchange='', routing_key=self.queue_name, body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )

    def close(self):
        self.connection.close()


class WorkerQueue(Worker):
    def __init__(self, worker_name, queue_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker_name = worker_name
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def worker(self):
        self.preset_worker()
        print(' ***Listening for messages...')

        def callback(ch, method, properties, body):
            decoded_body = json.loads(body)
            # try:
            # TODO: Custom tasks here
            self.process_task(routing_key=method.routing_key, body=decoded_body)
            # except Exception as e:
            #     traceback.print_exception(type(e), e, e.__traceback__)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        self.channel.start_consuming()

    def preset_worker(self, *args, **kwargs):
        """ Runs once
        """
        super().preset_worker()

    def process_task(self, *args, **kwargs):
        """
            Default method:
            >> self.process_task(routing_key=method.routing_key, body=decoded_body)

            use kwargs.get('routing_key') and kwargs.get('body') to get values.
        """
        super().process_task()
        # print(f" [x] {kwargs.get('routing_key', '')} : {kwargs.get('body', '')}")


class ExchangeWorker(Worker):
    def __init__(self, exchange_name, routing_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exchange_name = exchange_name
        self.routing_key = routing_key

        self.channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
        self.result = self.channel.queue_declare('', exclusive=True)
        self.queue_name = self.result.method.queue
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue_name, routing_key=routing_key)

    def worker(self):
        self.preset_worker()
        print(' ***Listening for trades...')

        def callback(ch, method, properties, body):
            decoded_body = json.loads(body)

            # try:
            # TODO: Custom tasks here
            self.process_task(routing_key=method.routing_key, body=decoded_body)
            # except Exception as e:
            #     traceback.print_exception(type(e), e, e.__traceback__)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def preset_worker(self, *args, **kwargs):
        """ Runs once
        """
        super().preset_worker()

    def process_task(self, *args, **kwargs):
        """
            Default method:
            >> self.process_task(routing_key=method.routing_key, body=decoded_body)

            use kwargs.get('routing_key') and kwargs.get('body') to get values.
        """
        super().process_task()
        # print(f" [x] {kwargs.get('routing_key', '')} : {kwargs.get('body', '')}")
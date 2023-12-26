import pika
import logging

formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s',
                              "%m/%d/%Y %H:%M:%S")

username = os.environ.get('AMPQ_USERNAME')
password = os.environ.get('AMPQ_PASSWORD')
gce_external_ip = os.environ.get('AMPQ_GCE_HOST')

class AMQP:
    def __init__(self, local=False):
        self.local = local
        self.connection = self.get_connection(self.local)
        self.channel = self.get_channel(self.connection)

        self.transaction_logger = logging.getLogger("amqp")
        self.transaction_handler = logging.FileHandler('amqp.log')
        self.transaction_logger.setLevel(logging.INFO)
        self.transaction_handler.setFormatter(formatter)

    @staticmethod
    def get_connection(local):
        if local:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            return connection

        # Connect to GCE
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(gce_external_ip, 5672, '/', credentials, heartbeat=600)
        connection = pika.BlockingConnection(parameters)
        return connection

    @staticmethod
    def get_channel(connection, channel_number=None):
        channel = connection.channel(channel_number)
        return channel

    def connection_status(self):
        if not self.connection or self.connection.is_closed:
            return False
        return True

    def reconnect(self):
        self.transaction_logger.info("reconnect amqp")
        self.connection = self.get_connection(self.local)
        self.channel = self.get_channel(self.connection)





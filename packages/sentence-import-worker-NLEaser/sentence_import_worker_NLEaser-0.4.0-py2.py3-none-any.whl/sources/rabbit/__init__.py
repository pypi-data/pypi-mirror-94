import pika as pk

from nleaser_config import RABBIT_HOST, RABBIT_PASS, RABBIT_PORT, RABBIT_QUEUES, RABBIT_USER


class RabbitConector():
    rabbit_host = RABBIT_HOST
    rabbit_port = RABBIT_PORT
    rabbit_user = RABBIT_USER
    rabbit_pass = RABBIT_PASS
    channel: pk.adapters.blocking_connection.BlockingChannel = None

    def __init__(self, queue_name):
        self.exchange = RABBIT_QUEUES[queue_name]["exchange"]
        self.routing_key = RABBIT_QUEUES[queue_name]["routing_key"]
        self.queue = RABBIT_QUEUES[queue_name]["queue"]

    def connect(self):
        creds = pk.PlainCredentials(
            username=self.rabbit_user,
            password=self.rabbit_pass
        )
        params = pk.ConnectionParameters(
            host=self.rabbit_host,
            port=self.rabbit_port,
            credentials=creds,
            heartbeat=0
        )
        conn = pk.BlockingConnection(parameters=params)

        channel = conn.channel()
        channel.exchange_declare(
            exchange=self.exchange,
            durable=True
        )
        channel.queue_declare(
            queue=self.queue,
            durable=True
        )
        channel.queue_bind(
            exchange=self.exchange,
            queue=self.queue,
            routing_key=self.routing_key
        )

        self.channel = channel

        return channel

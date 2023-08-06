import pika as pk
from sources.rabbit import RabbitConector


class RabbitProducer(RabbitConector):

    def send_message(self, message):
        if self.channel is None:
            self.connect()

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,

            body=message.encode(),
            properties=pk.BasicProperties(
                delivery_mode=2
            )
        )
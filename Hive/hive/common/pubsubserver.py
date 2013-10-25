import pika
import sys
import logging


class PubSubServer(object):

    def __init__(self, name, host, routing_key):
        self.exchange = name
        self.host = host
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, type='topic')
        self.channel.basic_qos(prefetch_count=1)
        self.routing_key = routing_key
        self.logger = logging.getLogger(__name__)
        self.logger.info("Publish Server Started!")

    def publish_msg(self, msg, routing_key=None):
        if routing_key is None:
            routing_key = self.routing_key
        else:
            routing_key = self.routing_key + "." + routing_key
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=routing_key,
                                   body=msg)
        self.logger.info(
            "Publishing message: %s to routing key %s" %
            (msg, routing_key))

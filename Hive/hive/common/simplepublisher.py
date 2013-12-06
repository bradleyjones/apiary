import pika
import sys
import logging


class SimplePublisher(object):

    def __init__(self, name, host, username, password):
        self.exchange = name
        self.host = host
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, type='topic')
        self.channel.basic_qos(prefetch_count=1)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Simple Publisher connection made.")

    def publish_msg(self, msg, routing_key):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=routing_key,
                                   body=msg)
        self.logger.info(
            "Publishing message: %s to routing key %s on exchange %s" %
            (msg, routing_key, self.exchange))

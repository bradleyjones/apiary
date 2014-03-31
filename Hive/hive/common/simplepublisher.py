"""A simple class that provides methods for publishing messages onto a topic
exchange."""

import pika
import sys
import logging

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class SimplePublisher(object):

    def __init__(self, name, host="localhost", username="guest",
                 password="guest", channel=None):
        self.exchange = name
        self.host = host
        if(channel is None):
            self.credentials = pika.PlainCredentials(username, password)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, credentials=self.credentials))
            self.channel = self.connection.channel()
        else:
            self.channel = channel
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

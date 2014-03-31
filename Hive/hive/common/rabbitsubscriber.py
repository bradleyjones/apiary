"""
A helper class for wrapping the creation and consuming of a queue
using rabbit.
"""

import pika
import logging
import traceback
import time
from rpcresponse import RPCResponse
from uuid import getnode as get_mac
from pkg_resources import resource_string
from StringIO import StringIO
import json
from jsonschema import validate
import threading

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class RabbitSubscriber(threading.Thread):

    def __init__(self, name, host, router, username, password, routingkeys):
        super(RabbitSubscriber, self).__init__()
        self.daemon = True
        self.exchange = "apiary"
        self.routingkeys = routingkeys
        self.exchangetype = "topic"
        self.queue = name
        self.host = host
        self.connection = None
        self.channel = None
        self.closing = False
        self.router = router
        self.identifier = name
        self.credentials = pika.PlainCredentials(username, password)
        self.machineid = str(get_mac())
        self.consumer_tag = None
        self.schema = json.loads(
            resource_string(__name__,
                            'schemas/message_schema.js'))
        self.logger = logging.getLogger(__name__)
        self.logger.info("Identifier: %s", self.identifier)
        self.logger.info("Mac Address: %s", self.machineid)

    def run(self):
        try:
            self.connection = self.connect()
        except Exception:
            self.logger.error("Failed to Connect correctly!")
            self.stop()
        self.connection.ioloop.start()

    def connect(self):
        return pika.SelectConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=self.credentials),
            self.onconnection_open,
            stop_ioloop_on_close=False)

    def onconnection_open(self, unused_connection):
        self.logger.info("Server Connected!")
        self.connection.add_on_close_callback(self.onconnection_closed)
        self.connection.channel(on_open_callback=self.onchannel_open)

    def onconnection_closed(self, connection, reply_code, reply_text):
        self.channel = None
        if self.closing:
            self.connection.ioloop.stop()
        else:
            self.logger.warning(
                'RabbitMQ Connection lost, reopening in 5 seconds: (%s) %s',
                reply_code, reply_text)
            self.connection.add_timeout(5, self.reconnect)

    def closechannel(self):
        self.logger.info("Closing RabbitMQ Channel")
        self.channel.close()

    def onchannel_open(self, channel):
        self.channel = channel
        self.channel.add_on_close_callback(self.onchannel_closed)
        self.channel.exchange_declare(self.on_exchange_declareok,
                                      self.exchange,
                                      self.exchangetype)

    def on_exchange_declareok(self, unused_frame):
        self.channel.queue_declare(
            self.on_queue_declareok,
            self.queue,
            durable=True)

    def on_queue_declareok(self, method_frame):
        for key in self.routingkeys:
            self.channel.queue_bind(
                self.onbindok,
                self.queue,
                self.exchange,
                key)
            self.logger.info("Subscribed to %s" % key)
        self.channel.add_on_cancel_callback(self.onconsumer_cancelled)
        self.consumer_tag = self.channel.basic_consume(self.onRequest,
                                                       self.queue)

    def onbindok(self, unused_frame):
        pass

    def onchannel_closed(self, channel, reply_code, reply_text):
        self.connection.close()

    def onconsumer_cancelled(self, method_frame):
        self.logger.info('Consumer was cancelled remotely, shutting down: %r',
                         method_frame)
        if self.channel:
            self.channel.close()

    def reconnect(self):
        self.connection.ioloop.stop()
        if not self.closing:
            self.connection = self.connect()
            self.connection.ioloop.start()

    def stop(self):
        self.logger.info("Stopping RabbitMQ Connection...")
        self.closing = True
        if self.channel:
            self.logger.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            self.channel.basic_cancel(self.on_cancelok, self.consumer_tag)
        self.connection.ioloop.start()
        self.logger.info("RabbitMQ Connection Stopped")

    def on_cancelok(self, frame):
        self.logger.info(
            'RabbitMQ acknowledged the cancellation of the consumer')
        self.channel.close()
    # Parse the Request
    # Pass the Action and Data down to the action router
    # Make a response to send back to the client
    # Fire off responses and acknowledge message

    def onRequest(self, ch, method, props, body):
        starttime = time.time()

        request = {}
        rpcresp = RPCResponse()

        try:
            request = self.jsonToHash(body)
            self.logger.info('Message Received: %s', str(request))
            request['routing_key'] = method.routing_key

            try:
                self.router(request["action"], request, rpcresp, self.channel)
            except Exception as e:
                self.logger.error(
                    'Inner Error Occured: %s',
                    traceback.format_exc())
        except Exception as e:
            self.logger.error(
                'Outer Error Occured: %s',
                traceback.format_exc())

        ch.basic_ack(delivery_tag=method.delivery_tag)

        timetaken = (time.time() - starttime)
        self.logger.info('Request Completed in %s seconds', str(timetaken))

    # Parse XML into a dictionary
    def jsonToHash(self, string):
        response = json.loads(string)
        validate(response, self.schema)
        return response


class RPCServerException(Exception):
    pass

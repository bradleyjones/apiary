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


class RPCServer(object):

    def __init__(self, name, host, func):
        self.queue = name
        self.host = host
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.router = func
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.onRequest, queue=self.queue)
        self.identifier = name
        self.machineid = str(get_mac())
        self.schema = json.loads(resource_string(__name__, 'schemas/message_schema.js'))
        self.logger = logging.getLogger(__name__)
        self.logger.info("Identifier: %s", self.identifier)
        self.logger.info("Mac Address: %s", self.machineid)
        self.logger.info("Server Started, Ready for Requests!")
        self.channel.start_consuming()

    # Parse the Request
    # Pass the Action and Data down to the action router
    # Make a response to send back to the client
    # Fire off responses and acknowledge message
    def onRequest(self, ch, method, props, body):
        starttime = time.time()

        request = {}
        rpcresp = RPCResponse()
        response = "INVALID MESSAGE RECEIVED"

        try:
            request = self.jsonToHash(body)
            self.logger.info('Message Received: %s', str(request))

            try:
                self.router(request["action"], request["data"], rpcresp)
            except Exception as e:
                rpcresp.action = "Error"
                rpcresp.data = traceback.format_exc()
                self.logger.error('Inner Error Occured: %s', rpcresp.data)
        except Exception as e:
            rpcresp.action = "Error"
            rpcresp.data = traceback.format_exc()
            request['from'] = "Unknown"
            self.logger.error('Outer Error Occured: %s', traceback.format_exc())

        self.logger.info('Responding with %s', rpcresp.data)
        response = self.makeResponse(request, rpcresp)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=
                                                         props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        timetaken = (time.time() - starttime)
        self.logger.info('Request Completed in %s seconds', str(timetaken))

    # Parse XML into a dictionary
    def jsonToHash(self, string):
        response = json.loads(string)
        validate(response, self.schema)
        return response

    def makeResponse(self, request, rpcresp):
        response = {}
        response['action'] = rpcresp.action
        response['to'] = request['from']
        response['from'] = self.identifier
        response['data'] = rpcresp.data
        response['machineid'] = self.machineid
        return json.dumps(response)


class RPCServerException(Exception):
    pass


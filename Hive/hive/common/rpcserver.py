"""
A helper class for wrapping the creation and consuming of a queue
using rabbit.
"""

import pika
import xml.etree.cElementTree as ET
import logging
import traceback
import time
from uuid import getnode as get_mac
from lxml import etree
from pkg_resources import resource_string
from StringIO import StringIO 


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
        self.schema = etree.XMLSchema(etree.parse(StringIO(resource_string(__name__, 'schemas/message_schema.xsd'))))
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
        action = "ERROR"
        response = "INVALID MESSAGE RECEIVED"
        
        try:
            request = self.xmlStringToHash(body)
            self.logger.info('Message Received from %s', request["from"])

            try:
                data = self.router(request["action"], request["data"])
                action = "DONE"
            except Exception as e:
                data = traceback.format_exc()
                self.logger.error('Error Occured: %s', data)

            response = self.makeResponse(action, request, data)
            self.logger.info('Responding with %s', data)
        except Exception as e:
            self.logger.error('Error Occured: %s', traceback.format_exc())

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=
                                                         props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        timetaken = (time.time() - starttime)
        self.logger.info('Request Completed in %s seconds', str(timetaken))

    def validateRequest(self, request):
        return self.schema.validate(etree.parse(StringIO(request)))

    # Parse XML into a dictionary
    def xmlStringToHash(self, string):
        if self.validateRequest(string):
            data = ET.fromstring(string)
            has = {}
            for child in data:
                has[child.tag] = child.text  
            return has
        else:
          raise RPCServerException("Invalid Message Received")

    def makeResponse(self, action, request, string):
        response = ET.Element('message')

        action = ET.SubElement(response, 'action')
        action.text = action

        to = ET.SubElement(response, 'to')
        to.text = request['from']

        fro = ET.SubElement(response, 'from')
        fro.text = self.identifier

        data = ET.SubElement(response, 'data')
        data.text = string

        machineid = ET.SubElement(response, 'machineid')
        machineid.text = self.machineid

        return ET.tostring(response, encoding='utf8', method='xml')

class RPCServerException(Exception):
  pass

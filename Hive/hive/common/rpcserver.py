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
        logging.info("Identifier: %s", self.identifier)
        logging.info("Mac Address: %s", self.machineid)
        logging.info("Server Started, Ready for Requests!")
        self.channel.start_consuming()

    # Parse the Request
    # Pass the Action and Data down to the action router
    # Make a response to send back to the client
    # Fire off responses and acknowledge message
    def onRequest(self, ch, method, props, body):
        starttime = time.time() 
        request = self.xmlStringToHash(body)

        logging.info('Message Received from %s', request["fro"])

        data = None
        action = "ERROR"

        try:
            data = self.router(request["action"], request["data"])
            action = "DONE"
        except Exception as e:
            data = traceback.format_exc()

        response = self.makeResponse(action, request, data)

        logging.info('Responding with %s', data)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=
                                                         props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        timetaken = (time.time() - starttime)
        logging.info('Request Completed in %s seconds', str(timetaken))

    # Parse XML into a dictionary
    def xmlStringToHash(self, string):
        data = ET.fromstring(string)
        has = {}
        for child in data:
            has[child.tag] = child.text
        return has

    def makeResponse(self, action, request, string):
        response = ET.Element('message')

        action = ET.SubElement(response, 'action')
        action.text = action

        to = ET.SubElement(response, 'to')
        to.text = request['fro']

        fro = ET.SubElement(response, 'fro')
        fro.text = self.identifier

        data = ET.SubElement(response, 'data')
        data.text = string

        machineid = ET.SubElement(response, 'machineid')
        machineid.text = self.machineid

        return ET.tostring(response, encoding='utf8', method='xml')

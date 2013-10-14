"""
A helper class for wrapping the creation and consuming of a queue
using rabbit.
"""

import pika
import xml.etree.cElementTree as ET
import logging

class RPCServer(object):

  def __init__(self, name, host, func):
    self.queue = name
    self.host = host
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
    self.channel = self.connection.channel()
    self.router = func
    self.channel.queue_declare(queue=self.queue)
    self.channel.basic_qos(prefetch_count=1)
    self.channel.basic_consume(self.onRequest, queue=self.queue)
    logging.info("Server Started, Ready for Requests!")
    self.channel.start_consuming()

  # Parse the Request
  # Pass the Action and Data down to the action router
  # Make a response to send back to the client
  # Fire off responses and acknowledge message
  def onRequest(self, ch, method, props, body):
    request = xmlStringToHash(body) 
    logging.debug('Message Received from %s', request["from"])
    data = self.func(request["action"], request["data"])
    response = makeResponse(request, data)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag= method.delivery_tag)

  # Parse XML into a dictionary 
  def xmlStringToHash(self, string):
    data = ET.fromstring(string)
    has = {}
    for child in root:
      has[child.tag] = child.text 
    return has

  def makeResponse(self, request, data):
    response = ET.Element('message')

    action = ET.SubElement(response, 'action')
    action = 'DONE'

    to = ET.SubElement(response, 'to')
    to.text = request['from']

    fro = ET.SubElement(response, 'fro')
    fro.text = self.identifier

    data = ET.SubElement(response, 'data')
    data.text = data

    machineid = ET.SubElement(response, 'machineid')
    machineid.text = self.machineid

    return ET.dump(response)

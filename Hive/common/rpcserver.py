"""
A helper class for wrapping the creation and consuming of a queue
using rabbit.
"""

import pika
import xml.etree.cElementTree as ET

class RPCServer(object):

  def __init__(self, name, host, func):
    self.queue = name
    self.host = host
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
    self.channel = connection.channel()
    self.router = func
    channel.queue_declare(queue=self.queue)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(onRequest, queue=queue)
    channel.start_consuming()
    print "Server Started, Ready for Requests!"

  def onRequest(self, ch, method, props, body):
    # Parse the Request
    request = xmlStringToHash(body) 
   
    # Pass the Action and Data down to the action router
    data = self.func(request["action"], request["data"])

    # Make a response to send back to the client
    response = makeResponse(request, data)
    
    # Fire off responses and acknowledge message
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag= method.delivery_tag)

  def xmlStringToHash(self, string):
    # Parse XML into a dictionary 
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

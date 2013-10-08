#!/usr/bin/env python
import pika
from ..helpers.rpcserver import RPCServer
from configobj import ConfigObj
import xml.etree.cElementTree as ET

rabbit_ip = None

def load_config():
  global rabbit_ip
  config = ConfigObj('honeycomb_config.ini')
  rabbit_ip = config['rabbit_ip']

def on_request(ch, method, props, body):
  # Read XML Body
  data = ET.fromstring(body)
  for child in data:
    print child.tag, child.attrib

  # Perform some action 
  response="Done."

  # Reply to RPC Request
  ch.basic_publish(exchange='',
                   routing_key=props.reply_to,
                   properties=pika.BasicProperties(correlation_id = \
                                                   props.correlation_id),
                   body="")
  ch.basic_ack(delivery_tag= method.delivery_tag)

##############################################################
# Below this point are methods which are called from a request

def index(data):
  """Takes a record from worker and indexes it into the DB"""
  return;

load_config()
print "Setting Up Server on %s" % rabbit_ip
server = RPCServer("honeycomb", rabbit_ip, on_request)

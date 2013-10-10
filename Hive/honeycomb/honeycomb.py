#!/usr/bin/env python
import pika
from ..helpers.rpcserver import RPCServer
from configobj import ConfigObj
import xml.etree.cElementTree as ET

rabbit_ip = None
server = None

def load_config():
  global rabbit_ip
  config = ConfigObj('honeycomb_config.ini')
  rabbit_ip = config['rabbit_ip']

def actionRouter(action, data):
  # Perform some action 
  response="Done."

  return response


##############################################################
# Below this point are methods which are called from a request

def index(data):
  """Takes a record from worker and indexes it into the DB"""
  return;

load_config()
print "Setting Up Server on %s" % rabbit_ip
server = RPCServer("honeycomb", rabbit_ip, actionRouter)

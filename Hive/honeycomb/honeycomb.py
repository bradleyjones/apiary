#!/usr/bin/env python
import pika
from ..common.rpcserver import RPCServer
from configobj import ConfigObj
import xml.etree.cElementTree as ET
import Routes
import Controller

rabbit_ip = None
server = None
cont = Controller()
router = Routes(cont)

def load_config():
  global rabbit_ip
  config = ConfigObj('honeycomb_config.ini')
  rabbit_ip = config['rabbit_ip']

load_config()
print "Setting Up Server on %s" % rabbit_ip
server = RPCServer("honeycomb", rabbit_ip, router.route)

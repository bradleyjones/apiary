#!/usr/bin/env python
from ..common.rpcserver import RPCServer
from configobj import ConfigObj
import controller
import routes

rabbit_ip = None
cont = controller.Controller()
router = routes.Routes(cont)

def load_config():
  global rabbit_ip
  config = ConfigObj('control_config.ini')
  rabbit_ip = config['rabbit_ip']

load_config()
print "Setting Up Server on %s" % rabbit_ip
server = RPCServer("control", rabbit_ip, router.route)

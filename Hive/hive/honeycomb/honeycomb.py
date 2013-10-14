#!/usr/bin/env python
from ..common.rpcserver import RPCServer
from configobj import ConfigObj
import controller
import routes
from ..common import logger

def load_config():
  logger.configureLogger('honeycomb.log')
  return ConfigObj('honeycomb_config.ini')

def main():
  cont = controller.Controller()
  router = routes.Routes(cont)
  config = load_config()
  print "Setting Up Server on %s" % config['rabbit_ip']
  server = RPCServer("honeycomb", config['rabbit_ip'], router.route)

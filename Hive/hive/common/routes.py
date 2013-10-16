import logging
import routingexception

class Routes(object): 

  def __init__(self, controller): 
    self.routes = {}
    self.controller = controller
    self.setupRoutes()
    print "Routes Loaded:"
    print self.routes.keys() 

  def setupRoutes(self):
    return

  def route(self, action, data):
    if action in self.routes:
      try:
        logging.debug("Route %s calling function %s", action, self.routes[action]) 
        return self.routes[action](data)
      except NameError as e:
        raise RoutingException("Action not found in controller: " + self.routes[action])
    else 
      raise RoutingException("Route not found for: " + action)  

  def action(self, name, func):
    if name in self.routes
      raise RoutingException("Route already exists: " + name) 
    else
      self.routes[name] = func

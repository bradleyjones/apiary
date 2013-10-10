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
    return self.routes[action](data)

  def action(self, name, func):
    self.routes[name] = func

from ..common.routes import Routes as Parent

class Routes(Parent):
  def setupRoutes(self):
    action("insert", self.controller.default)
    action("wobble", self.controller.default)

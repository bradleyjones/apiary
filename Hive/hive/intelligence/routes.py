from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        self.action("insert", self.controller.default)
        self.action("wobble", self.controller.default)

from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        self.action("GET", "get")

from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        self.action("HANDSHAKE", self.controller.handshake)

        self.action("wobble", self.controller.default)

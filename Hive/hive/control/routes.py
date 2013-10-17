from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        self.action("HANDSHAKE", "handshake")
        self.action("AGENTS", "get_agents")
        self.action("GOODBYE", "goodbye")

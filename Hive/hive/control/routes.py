from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        self.action("HANDSHAKE", "handshake")
        self.action("HEARTBEAT", "heartbeat")
        self.action("ALLAGENTS", "get_agents")
        self.action("AUTHENTICATE", "authenticate")
        self.action("SINGLEAGENT", "get_single_agent")
        self.action("GOODBYE", "goodbye")

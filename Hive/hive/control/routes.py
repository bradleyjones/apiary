from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        # RPC Controller Actions
        self.action("HANDSHAKE", "handshake", 'hive.control.agentscontroller')
        self.action("ALLAGENTS", "get_agents", 'hive.control.agentscontroller')
        self.action(
            "AUTHENTICATE",
            "authenticate",
            'hive.control.agentscontroller')
        self.action(
            "RELEASE",
            "release",
            'hive.control.agentscontroller')
        self.action(
            "SINGLEAGENT",
            "get_single_agent",
            'hive.control.agentscontroller')
        self.action("GOODBYE", "goodbye", 'hive.control.agentscontroller')
        # Subcontroller Actions
        self.action("HEARTBEAT", "heartbeat", 'hive.control.agentscontroller')

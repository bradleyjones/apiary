from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        # RPC Controller Actions
        self.action("HANDSHAKE", "handshake", 'hive.control.rpccontroller')
        self.action("ALLAGENTS", "get_agents", 'hive.control.rpccontroller')
        self.action(
            "AUTHENTICATE",
            "authenticate",
            'hive.control.rpccontroller')
        self.action(
            "SINGLEAGENT",
            "get_single_agent",
            'hive.control.rpccontroller')
        self.action("GOODBYE", "goodbye", 'hive.control.rpccontroller')
        # Subcontroller Actions
        self.action("HEARTBEAT", "heartbeat", 'hive.control.subcontroller')

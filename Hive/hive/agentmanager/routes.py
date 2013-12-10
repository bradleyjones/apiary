from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        # Agent Controller Actions
        self.action(
            "HANDSHAKE",
            "handshake",
            'hive.agentmanager.agentscontroller')
        self.action(
            "UPDATE",
            "update",
            'hive.agentmanager.agentscontroller')
        self.action(
            "ALLAGENTS",
            "get_agents",
            'hive.agentmanager.agentscontroller')
        self.action(
            "AGENTSCOUNT",
            "get_agents_count",
            'hive.agentmanager.agentscontroller')
        self.action(
            "AUTHENTICATE",
            "authenticate",
            'hive.agentmanager.agentscontroller')
        self.action(
            "RELEASE",
            "release",
            'hive.agentmanager.agentscontroller')
        self.action(
            "SINGLEAGENT",
            "get_single_agent",
            'hive.agentmanager.agentscontroller')
        self.action(
            "GOODBYE",
            "goodbye",
            'hive.agentmanager.agentscontroller')
        self.action(
            "HEARTBEAT",
            "heartbeat",
            'hive.agentmanager.agentscontroller')

        # Config Controller Actions
        self.action(
            "SETFILES",
            "setFiles",
            "hive.agentmanager.configcontroller")

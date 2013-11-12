from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        self.action("GET", "get", "hive.honeycomb.rpccontroller")
        self.action("SUBSCRIBE", "subscribe", "hive.honeycomb.rpccontroller")
        self.action("DATA", "data", "hive.honeycomb.subcontroller")

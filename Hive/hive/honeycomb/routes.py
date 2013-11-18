from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        self.action("SUBSCRIBE", "subscribe", "hive.honeycomb.maincontroller")
        self.action(
            "UNSUBSCRIBE",
            "unsubscribe",
            "hive.honeycomb.maincontroller")

        self.action("INSERT", "insert", "hive.honeycomb.databasecontroller")
        self.action("GET", "get", "hive.honeycomb.databasecontroller")

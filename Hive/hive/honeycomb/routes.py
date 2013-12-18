from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        self.action("DATA", "insert", "hive.honeycomb.databasecontroller")
        self.action("FIND", "find", "hive.honeycomb.databasecontroller")
        self.action("COUNT", "count", "hive.honeycomb.databasecontroller")
        self.action("FINDALL", "findall", "hive.honeycomb.databasecontroller")

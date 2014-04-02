"""Routes for Honeycomb Actions."""

from ..common.routes import Routes as Parent

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Routes(Parent):

    def setupRoutes(self):
        self.action("DATA", "insert", "hive.honeycomb.databasecontroller")
        self.action("FIND", "find", "hive.honeycomb.databasecontroller")
        self.action("COUNT", "count", "hive.honeycomb.databasecontroller")
        self.action("FINDALL", "findall", "hive.honeycomb.databasecontroller")
        self.action("QUERY", "query", "hive.honeycomb.databasecontroller")
        self.action(
            "REBUILD",
            "rebuildIndexes",
            "hive.honeycomb.databasecontroller")

        self.action("SEARCH", "newsearch", "hive.honeycomb.searchcontroller")
        self.action("STOPSEARCH", "stop", "hive.honeycomb.searchcontroller")

        self.action(
            "TIMESTAMPS",
            "timestamps",
            "hive.honeycomb.querycontroller")

        self.action(
            "TAGS",
            "tags",
            "hive.honeycomb.querycontroller")

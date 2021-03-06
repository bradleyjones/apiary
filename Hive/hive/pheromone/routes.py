"""Routes for the Pheromone RPC and work Actions."""

from ..common.routes import Routes as Parent

__author__ = "Sam Betts, Bradley Jones"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Routes(Parent):

    def setupRoutes(self):
        # Agent Controller Actions
        self.action("ALL", "get_all", 'hive.pheromone.controller')
        self.action("NEW", "new", 'hive.pheromone.controller')
        self.action("DELETE", "delete", 'hive.pheromone.controller')

from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        # Agent Controller Actions
        self.action("ALL", "get_all", 'hive.pheromone.controller')
        self.action("NEW", "new", 'hive.pheromone.controller')
        self.action("DELETE", "delete", 'hive.pheromone.controller')

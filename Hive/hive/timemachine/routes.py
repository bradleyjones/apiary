from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        # Agent Controller Actions
        self.action("NEW", "new", 'hive.timemachine.controller')
        self.action("DELETE", "delete", 'hive.timemachine.controller')

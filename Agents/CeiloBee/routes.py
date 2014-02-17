from hive.common.routes import Routes as Parent

class Routes(Parent):

    def setupRoutes(self):
        # CeiloBee Controller Actions
        
        self.action(
            "DONE",
            "handshake",
            'celiobee.controllers')
            
        self.action(
            "CREATEOPENSTACK",
            "createOpenstack",
            'celiobee.controllers')
        self.action(
            "REMOVEOPENSTACK",
            "removeOpenstack",
            'celiobee.controllers')
        self.action(
            "GETOPENSTACKS",
            "getOpenstacks",
            'celiobee.controllers')

        self.action(
            "GETMETERS",
            "getMeters",
            'celiobee.controllers')
        self.action(
            "CREATELISTENER",
            "createListener",
            'celiobee.controllers')
        self.action(
            "DELETELISTENER",
            "deleteListener",
            'celiobee.controllers')

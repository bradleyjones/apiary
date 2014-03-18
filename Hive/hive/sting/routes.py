from ..common.routes import Routes as Parent


class Routes(Parent):

    def setupRoutes(self):
        # Sting Actions
        self.action(
            "CALLBACK",
            "callback",
            'hive.sting.stingcontroller')
        self.action(
            "NEWCHANNEL",
            "new_channel",
            'hive.sting.stingcontroller')

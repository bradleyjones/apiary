from ..common.routes import Routes as Parent

__author__ = "John Davidge"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


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
        self.action(
            "EVENT",
            "event",
            'hive.sting.stingcontroller')

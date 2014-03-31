"""Extends the common.model this is the Database model used to store
information about Agents."""

from ..common.model import Model

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Agent(Model):

    def define(self):
        self.addcolumn('UUID')
        self.addcolumn('HEARTBEAT')
        self.addcolumn('DEAD')
        self.addcolumn('AUTHENTICATED')
        self.addcolumn('BOUND')
        self.addcolumn('QUEUE')
        self.addcolumn('MACHINEID')
        self.addcolumn('METADATA')
        self.setprimary('UUID')

from ..common.model import Model


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

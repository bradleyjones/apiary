import sqlite3
from ..common.model import Model


class Agent(Model):

    def define(self):
        self.addcolumn('UUID')
        self.addcolumn('HEARTBEAT')
        self.addcolumn('DEAD')
        self.addcolumn('AUTHENTICATED')
        self.addcolumn('BOUND')
        self.addcolumn('QUEUE')
        self.setprimary('UUID')

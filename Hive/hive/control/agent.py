import sqlite3
from ..common.model import Model

class Agent(Model):

    def define(self):
        self.addcolumn('UUID', 'TEXT') 
        self.addcolumn('HEARTBEAT', 'REAL')
        self.addcolumn('DEAD', 'INT')
        self.addcolumn('AUTHENTICATED', 'INT')
        self.setprimary('UUID')

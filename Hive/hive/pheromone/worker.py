"""Model for storing the info on the background Alerters in the database."""

from hive.common.model import Model

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Worker(Model):

    def define(self):
        self.addcolumn('CONTROLQUEUE')
        self.addcolumn('UUID')
        self.addcolumn('QUERY')
        self.addcolumn('QUANTITY')
        self.addcolumn('TIME')
        self.addcolumn('MESSAGE')
        self.setprimary('CONTROLQUEUE')

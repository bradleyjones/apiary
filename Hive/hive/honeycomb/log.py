"""Model representing Log data stored in Honeycomb, defines the indexes and
fields."""

from ..common.model import Model

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Log(Model):

    def define(self):
        self.addcolumn('CONTENT')
        self.addcolumn('TYPE')
        self.addcolumn('EVENTTIMESTAMP')
        self.addcolumn('METADATA')
        self.addindex('CONTENT')
        self.addindex('EVENTTIMESTAMP')
        self.addindex('TYPE')
        self.addindex('METADATA')

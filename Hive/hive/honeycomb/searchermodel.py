"""Model for storing the information about background recurring searches."""

from hive.common.model import Model

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class SearcherModel(Model):

    def define(self):
        self.addcolumn('CONTROLQUEUE')
        self.addcolumn('OUTPUTEXCHANGE')
        self.addcolumn('QUERY')
        self.setprimary('CONTROLQUEUE')

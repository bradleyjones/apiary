from ..common.model import Model

__author__ = "John Davidge"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class device(Model):

    def define(self):
        self.addcolumn('device_name')
        self.addcolumn('device_id')

from ..common.model import Model


class device(Model):

    def define(self):
        self.addcolumn('device_name')
        self.addcolumn('device_id')

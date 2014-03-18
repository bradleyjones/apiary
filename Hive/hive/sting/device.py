from ..common.model import Model


class device(Model):

    def define(self):
        self.addcolumn('UUID')
        self.addcolumn('NAME')
        self.addcolumn('DEVICE_ID')
        self.setprimary('UUID')

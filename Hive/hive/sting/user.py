from ..common.model import Model


class user(Model):

    def define(self):
        self.addcolumn('UUID')
        self.addcolumn('USERNAME')
        self.addcolumn('DEVICE')
        self.setprimary('UUID')

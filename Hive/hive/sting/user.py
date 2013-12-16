from ..common.model import Model


class User(Model):

    def define(self):
        self.addcolumn('UUID')
        self.addcolumn('USERNAME')
        self.addcolumn('DEVICE')
        self.addcolumn('NOTIFICATIONS')
        self.setprimary('UUID')

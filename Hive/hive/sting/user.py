from ..common.model import Model


class user(Model):

    def define(self):
        self.addcolumn('username')
        self.addcolumn('devices')

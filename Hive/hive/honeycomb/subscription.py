from ..common.model import Model


class Subscription(Model):

    def define(self):
        self.addcolumn('UUID', 'TEXT')
        self.addcolumn('AUTHENTICATED', 'BOOL')
        self.addcolumn('BOUND', 'BOOL')
        self.setprimary('UUID')

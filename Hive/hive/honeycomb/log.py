from ..common.model import Model


class Log(Model):

    def define(self):
        self.addcolumn('CONTENT')
        self.addcolumn('TYPE')
        self.addcolumn('TIMESTAMP')
        self.addcolumn('METADATA')
        self.addindex('CONTENT')
        self.addindex('TIMESTAMP')
        self.addindex('TYPE')
        self.setprimary('UUID')

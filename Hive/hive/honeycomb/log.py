from ..common.model import Model


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

from hive.common.model import Model


class Worker(Model):

    def define(self):
        self.addcolumn('CONTROLQUEUE')
        self.addcolumn('OUTPUTQUEUE')
        self.addcolumn('QUERY')
        self.addcolumn('QUANTITY')
        self.addcolumn('TIME')
        self.setprimary('CONTROLQUEUE')

from hive.common.model import Model


class SearcherModel(Model):

    def define(self):
        self.addcolumn('CONTROLQUEUE')
        self.addcolumn('OUTPUTEXCHANGE')
        self.addcolumn('QUERY')
        self.setprimary('CONTROLQUEUE')

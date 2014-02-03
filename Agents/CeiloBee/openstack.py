from hive.common.model import Model


class Openstack(Model):

    def define(self):
        self.addcolumn('IP')
        self.addcolumn('LOGIN')
        self.addcolumn('PASSWORD')
        self.addcolumn('AUTHTOKEN')
        self.addcolumn('CEILOIP')

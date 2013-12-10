from pymongo import MongoClient


class Driver(object):

    def __init__(self, config, tablename):
        self.client = MongoClient(
            "mongodb://%s:%s" % (config['Database']['mongodb_host'],
                                 config['Database']['mongodb_port']))
        self.columns = []
        self.config = config
        self.tablename = self.__class__.__name__ + "s"
        self.name = config['Database'][tablename]
        self.table = self.client[self.name][self.tablename]

    def index(self, fields, record):
        for field in fields:
            self.table.ensureIndex({field: "text"})

    def updateindex(self, fields, record):
        for field in fields:
            self.table.ensureIndex({field: "text"})

    def removeindex(self, fields, record):
        pass

    def query(self, query):
        q = self.table.runCommand("text", {search: query})

        return q['results']

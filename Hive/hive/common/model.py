from pymongo import MongoClient
from collections import OrderedDict
import logging


class ModelObject(object):

    def __init__(self, columns, data):
        self.columns = columns
        for col in columns:
            if col in data:
                setattr(self, col, data[col])
            else:
                setattr(self, col, None)

    def to_hash(self):
        resp = {}
        for col in self.columns:
            resp[col] = getattr(self, col)
        return resp


class Model(object):

    def __init__(self, config):
        # Database Connection Config
        self.client = MongoClient(
            "mongodb://%s:%s" % (config['Database']['mongodb_host'],
                                 config['Database']['mongodb_port']))
        self.tablename = self.__class__.__name__ + "s"
        self.name = config['Database']['name']
        self.table = self.client[self.name][self.tablename]

        # Model information variables
        self.columns = []
        self.indexes = []
        self.primary = None
        self.define()

        self.logger = logging.getLogger(__name__)
        self.indexdriver = self.loadIndexDriver()

    # Functions for loading the indexer
    def loadIndexDriver(self):
        if len(self.indexes) > 0:
            return (
                self.my_import(
                    self.config[
                        'Database'][
                        'indexdriver']).Driver(
                    self.config)
            )
        else:
            return None

    def my_import(self, name):
        __import__(name)
        return sys.modules[name]

    # Functions for defining Model
    def define(self):
        raise NotImplementedError()

    def addcolumn(self, name):
        if name in self.columns:
            raise Exception("Can't have duplicate column names")
        self.columns.append(name)

    def addindex(self, name):
        if not (name in self.columns):
            raise Exception("Can't index noexistant column")
        self.indexes.append(name)

    def setprimary(self, name):
        if self.primary is None:
            self.primary = name
        else:
            raise Exception("Can't define primary key twice")

    # Functions for manipulating model
    def new(self):
        return ModelObject(self.columns, {})

    def save(self, model):
        query = {self.primary: getattr(model, self.primary)}
        obj = {}
        record = self.table.find_one(query)
        if record is None:
            self.logger.info("Creating new record in the DB")
        else:
            obj = record
            self.logger.info("Updating record in the DB")

        # Add columns to hash
        for col in self.columns:
            obj[col] = getattr(model, col)

        objid = self.table.save(obj)
        obj['_id'] = objid

        # If index driver exists then index baby!
        if self.indexdriver:
            if record is None:
                self.indexdriver.index(self.indexes, obj)
            else:
                self.indexdriver.updateindex(self.indexes, obj)

        return obj

    def delete(self, model):
        query = {self.primary: getattr(model, self.primary)}
        self.table.remove(query)
        if self.indexdriver:
            self.indexdriver.removeindex(model)

    def query(self, query):
        pass

    def findAll(self):
        result = self.table.find({})
        response = []
        for res in result:
            response.append(ModelObject(self.columns, res))
        return response

    def find(self, id):
        query = {self.primary: id}
        record = self.table.find_one(query)
        if record is None:
            return None
        response = ModelObject(self.columns, record)
        return response

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
        self.client = MongoClient("mongodb://%s:%s" % (config['Database']['mongodb_host'],
                    config['Database']['mongodb_port']))
        self.columns = []
        self.tablename = self.__class__.__name__ + "s"
        self.name = config['Database']['name']
        self.table = self.client[self.name][self.tablename]
        self.primary = None
        self.logger = logging.getLogger(__name__)
        self.define()

    def addcolumn(self, name):
        if name in self.columns:
            raise Exception("Can't have duplicate column names")
        self.columns.append(name)

    def setprimary(self, name):
        if self.primary is None:
            self.primary = name
        else:
            raise Exception("Can't define primary key twice")

    def define(self):
        raise NotImplementedError()

    def new(self):
        return ModelObject(self.columns, {})

    def save(self, model):
        query = { self.primary:getattr(model, self.primary) }
        record = self.table.find_one(query)
        if record is None:
          record = {}
          self.logger.info("Creating new record in the DB")
        else:
          self.logger.info("Updating record in the DB")
        for col in self.columns:
          record[col] = getattr(model, col)
        self.table.save(record)

    def delete(self, model):
        query = { self.primary:getattr(model, self.primary) }
        self.table.remove(query)

    def findAll(self):
        result = self.table.find({})
        response = []
        for res in result: 
            response.append(ModelObject(self.columns, res))
        return response

    def find(self, id):
        query = { self.primary:id }
        record = self.table.find_one(query)
        if record is None:
          return None
        response = ModelObject(self.columns, record)
        return response

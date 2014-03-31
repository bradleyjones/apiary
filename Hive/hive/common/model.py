from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import OrderedDict
import logging
import sys
import datetime
import pytz

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


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
        self.config = config
        # Database Connection Config
        self.client = MongoClient(
            "mongodb://%s:%s" % (config['Database']['mongodb_host'],
                                 config['Database']['mongodb_port']))
        self.tablename = self.__class__.__name__ + "s"
        self.name = config['Database']['name']
        self.table = self.client[self.name][self.tablename]

        # Model information variables
        self.primary = '_id'
        self.columns = ['TIMESTAMP']
        self.indexes = []
        self.define()

        if (self.primary is '_id') and not ('_id' in self.columns):
            self.columns.append('_id')

        self.logger = logging.getLogger(__name__)
        self.indexdriver = self.loadIndexDriver()

    # Functions for loading the indexer
    def loadIndexDriver(self):
        if len(self.indexes) > 0:
            if 'indexdriver' in self.config['Database']:
                return (
                    self.my_import(
                        self.config[
                            'Database'][
                            'indexdriver']).Driver(
                        self.config, self.tablename)
                )
        return None

    def rebuildIndex(self):
        re = self.findAll()
        data = []
        for r in re:
            data.append(r.to_hash())
        self.indexdriver.rebuildIndex(self.indexes, data)
        return True

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
        if self.primary is '_id':
            self.primary = name
        else:
            raise Exception("Can't define primary key twice")

    # Functions for manipulating model
    def new(self):
        return ModelObject(self.columns, {})

    def save(self, model):
        obj = {}
        record = None

        if getattr(model, self.primary) is not None:
            query = {self.primary: getattr(model, self.primary)}
            record = self.table.find_one(query)

        if record is None:
            self.logger.info("Creating new record in the DB")
        else:
            obj = record
            self.logger.info("Updating record in the DB")

        # Add columns to hash
        for col in self.columns:
            d = getattr(model, col)
            if d is not None:
                obj[col] = d

        objid = self.table.save(obj)
        obj['_id'] = objid

        if isinstance(obj['_id'], ObjectId):
            obj['_id'] = str(obj['_id'])
            obj['TIMESTAMP'] = str(objid.generation_time)

        # If index driver exists then index baby!
        if self.indexdriver:
            if record is None:
                self.indexdriver.index(self.indexes, obj)
            else:
                self.indexdriver.updateindex(self.indexes, obj)

        return ModelObject(self.columns, obj)

    def delete(self, model):
        query = {self.primary: getattr(model, self.primary)}
        self.table.remove(query)
        if self.indexdriver:
            self.indexdriver.removeindex(model)

    def query(self, query, timescale):
        results = self.indexdriver.query(query)

        now = datetime.datetime.now(pytz.utc)
        response = {'totalHits': 0, 'hits': {}}

        query = {'$or': []}
        for hit in results['hits']:
            if self.primary == "_id":
                query['$or'].append({self.primary: ObjectId(hit)})
            else:
                query['$or'].append({self.primary: hit})

        if len(results['hits']) > 0:
            dbresult = self.table.find(query)
            for res in dbresult:
                time = res['_id'].generation_time
                if (now - time).total_seconds() < float(timescale):
                    res['TIMESTAMP'] = str(time)
                    res['_id'] = str(res['_id'])
                    response['hits'][str(res['_id'])] = {}
                    response['hits'][str(res['_id'])]['score'] = results[
                        'hits'][str(res['_id'])]['score']
                    response['hits'][str(res['_id'])]['log'] = ModelObject(
                        self.columns, res).to_hash()
                    response['totalHits'] = response['totalHits'] + 1

        return response

    def mongoQuery(self, query, fields={}):
        if len(fields) > 0:
            result = self.table.find(query, fields)
            newColumns = [self.primary, 'TIMESTAMP']
            for f in fields:
                newColumns.append(f)
        else:
            result = self.table.find(query)
            newColumns = self.columns

        response = []
        for res in result:
            res['TIMESTAMP'] = str(res['_id'].generation_time)
            res['_id'] = str(res['_id'])
            response.append(ModelObject(newColumns, res))
        return response

    def findAll(self):
        return self.mongoQuery({})

    def find(self, id):
        if self.primary == "_id" and not isinstance(id, ObjectId):
            id = ObjectId(id)
        query = {self.primary: id}
        record = self.table.find_one(query)
        if record is None:
            return None
        record['TIMESTAMP'] = str(record['_id'].generation_time)
        record['_id'] = str(record['_id'])
        response = ModelObject(self.columns, record)
        return response

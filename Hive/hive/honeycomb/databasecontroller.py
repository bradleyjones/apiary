from pymongo import MongoClient
from ..common.controller import Controller as Parent
import json
from bson.objectid import ObjectId

class Controller(Parent):

    def models(self):
        self.client = MongoClient("mongodb://%s:%s" % (self.config['Database']['mongodb_host'],
            self.config['Database']['mongodb_port']))
        self.logs = self.client['apiary']['logs']

    def insert(self, data, resp):
        self.logs.insert(json.loads(data['data']))
        resp.respond("OK")

    def find(self, data, resp):
        result = self.logs.find_one(json.loads(data['data']))
        result['_id'] = str(result['_id'])
        resp.respond(result)

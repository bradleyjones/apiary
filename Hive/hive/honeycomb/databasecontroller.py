from pymongo import MongoClient
from ..common.controller import Controller as Parent
import json
from bson.objectid import ObjectId


class Controller(Parent):

    def models(self):
        self.client = MongoClient(
            "mongodb://%s:%s" % (self.config['Database']['mongodb_host'],
                                 self.config['Database']['mongodb_port']))
        self.logs = self.client['apiary']['logs']

    def insert(self, msg, resp):
        self.logs.insert(json.loads(msg['data']))
        resp.respond("OK")

    def find(self, msg, resp):
        result = self.logs.find(json.loads(msg['data']))
        response = []
        for log in result:
            log['_id'] = str(log['_id'])
            response.append(log)
        resp.respond(response)

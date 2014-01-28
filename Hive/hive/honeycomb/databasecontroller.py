from pymongo import MongoClient
from ..common.controller import Controller as Parent
import json
from bson.objectid import ObjectId
from log import Log


class Controller(Parent):

    def models(self):
        self.logs = Log(self.config)

    def insert(self, msg, resp):
        data = json.loads(msg['data'])
        log = self.logs.new()
        log.CONTENT = data['CONTENT']
        log.TYPE = data['TYPE']
        log.EVENTTIMESTAMP = data['EVENTTIMESTAMP']        
        log.METADATA = data['METADATA']
        self.logs.save(log)
        resp.respond(log.to_hash())

    def find(self, msg, resp):
        resp.respond("WOOP")

    def findall(self, msg, resp):
        logs = self.logs.findAll()
        response = {}
        for log in logs:
            response[str(log._id)] = log.to_hash()
        resp.respond(json.dumps(response))

    def query(self, msg, resp):
        results = logs.query(msg['data'])
        resp.respond(results)

    def count(self, msg, resp):
        logs = self.logs.findAll()
        resp.respond(len(logs))

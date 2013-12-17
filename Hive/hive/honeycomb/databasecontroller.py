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

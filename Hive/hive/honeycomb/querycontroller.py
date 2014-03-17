from pymongo import MongoClient
from ..common.controller import Controller as Parent
from hive.common.rpcsender import RPCSender
import json
from bson.objectid import ObjectId
from log import Log


class Controller(Parent):

    def models(self):
        self.logs = Log(self.config)

    def timestamps(self, msg, resp):
        logs = self.logs.mongoQuery({}, {'EVENTTIMESTAMP' : 1})
        response = {}
        for log in logs:
            response[str(log._id)] = log.to_hash()
        resp.respond(response)

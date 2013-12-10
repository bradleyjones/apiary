from pymongo import MongoClient
from ..common.controller import Controller as Parent
import json
from bson.objectid import ObjectId
from log import Log


class Controller(Parent):

    def models(self):
        logs = Log(self.config)

    def insert(self, msg, resp):
        resp.respond("OK")

    def find(self, msg, resp):
        resp.respond("WOOP")

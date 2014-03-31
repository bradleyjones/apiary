"""Controller for Actions relating to Log data such as inserting or basic
querying."""

from pymongo import MongoClient
from ..common.controller import Controller as Parent
from hive.common.rpcsender import RPCSender
import json
from bson.objectid import ObjectId
from log import Log

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Controller(Parent):

    def models(self):
        self.logs = Log(self.config)

    def insert(self, msg, resp):
        log = self.logs.new()
        log.CONTENT = msg['data']['CONTENT']
        log.TYPE = msg['data']['TYPE']
        log.EVENTTIMESTAMP = msg['data']['EVENTTIMESTAMP']
        log.METADATA = msg['data']['METADATA']
        log = self.logs.save(log)
        resp.respond(log.to_hash())

    def rebuildIndexes(self, msg, resp):
        self.logs.rebuildIndex()
        resp.respond('DONE')

    def find(self, msg, resp):
        sender = RPCSender(self.config)
        resp.respond("WOOP")

    def findall(self, msg, resp):
        logs = self.logs.findAll()
        response = {}
        for log in logs:
            response[str(log._id)] = log.to_hash()
        resp.respond(response)

    def query(self, msg, resp):
        results = self.logs.query(
            msg['data']['QUERY'],
            msg['data']['TIMESCALE'])
        resp.respond(results)

    def count(self, msg, resp):
        logs = self.logs.findAll()
        resp.respond(len(logs))

from pymongo import MongoClient
from ..common.controller import Controller as Parent


class Controller(Parent):

    def models(self):
        self.client = MongoClient(
            self.config['Database']['mongodb_host'],
            self.config['Database']['mongodb_port'])
        self.logs = self.client['apiary']['logs']

    def insert(self, data, resp):
        self.logs.insert(data)
        resp.respond("OK")

    def find(self, data, resp):
        resp.respond(self.logs.find_one(data))

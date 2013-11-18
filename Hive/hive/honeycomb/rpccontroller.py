from pymongo import MongoClient
from ..common.controller import Controller as Parent
from subscription import Subscription

class Controller(Parent):

    def models(self):
        self.client = MongoClient('localhost', 27017)
        self.logs = self.client['apiary']['logs']
        self.subscriptions = Subscription(self.config)

    def subscribe(self, data, resp):
        sub = self.subscriptions.new()
        sub.UUID = data
        sub.AUTHENTICATED = True
        sub.BOUND = False
        self.subscriptions.save(sub)

    def unsubscribe(self, data, resp):
        sub = self.subscriptions.find(data)
        sub.AUTHENTICATED = False
        self.subscriptions.save(sub)

    def find(self, data, resp):
        self.logs.find_one(data)

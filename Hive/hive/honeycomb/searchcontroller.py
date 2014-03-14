from pymongo import MongoClient
from ..common.controller import Controller as Parent
from hive.common.rpcsender import RPCSender
import json
from bson.objectid import ObjectId
from log import Log
from hive.common.longrunningproc import ProcHandler
from hive.honeycomb.searchermodel import SearcherModel
from hive.honeycomb.searcher import Searcher

class Controller(Parent):

    def models(self):
        self.searchers = SearcherModel(self.config)

    def newsearch(self, msg, resp):
        searcher = self.searchers.new()

        sender = RPCSender(self.config)
        r = sender.channel.queue_declare() 
        q = r.method.queue

        machine = ProcHandler(self.config, Searcher(self.config, msg['data']['QUERY']), q)
        machine.start()
        
        searcher.OUTPUTQUEUE = sender.send_request('QUEUE', 'hive', {}, '', '', key=q)
        searcher.CONTROLQUEUE = q
        searcher.QUERY = msg['data']['QUERY']

        self.searchers.save(searcher)

        resp.respond(searcher.OUTPUTQUEUE)

    def stop(self, msg, resp):
        searcher = self.searchers.find(msg.data)
        pub = SimplePublisher(
            ''. self.config['Rabbit']['host'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['passwords'])
        pub.publish_msg(self, 'STOP', searcher.CONTROLQUEUE)

        resp.respond('DELETED')

from pymongo import MongoClient
from ..common.controller import Controller as Parent
import json
from bson.objectid import ObjectId
from log import Log
from seachermodel import SearcherModel
from searcher import Searcher

class Controller(Parent):

    def models(self):
        self.searchers = SearcherModel(self.config)

    def newsearch(self, msg, resp):
        searcher = self.searchers.new()
        
        machine = ProcHandler(self.config, Searcher(self.config, msg.data))
        machine.start()

        if(not machine.ready.wait(10)) {
            raise Exception("Long Running Process Failed to Start")
        }

        searcher.CONTROLQUEUE = machine.stopqueue
        searcher.OUTPUTQUEUE = machine.subproc.queue
        searcher.QUERY = msg.body

        self.seachers.save(searcher)

        resp.respond(searcher.OUTPUTQUEUE)
        

    def stop(self, msg, resp):
        searcher = self.searchers.find(msg.data)
        pub = SimplePublisher(
            ''. self.config['Rabbit']['host'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['passwords'])
        pub.publish_msg(self, 'STOP', searcher.CONTROLQUEUE)

        resp.respond('DELETED')

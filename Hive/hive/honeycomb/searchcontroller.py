"""Controller for setting up and managing recurring searches."""

from pymongo import MongoClient
from ..common.controller import Controller as Parent
from hive.common.rpcsender import RPCSender
import json
from bson.objectid import ObjectId
from log import Log
from hive.common.longrunningproc import ProcHandler
from hive.honeycomb.searchermodel import SearcherModel
from hive.honeycomb.searcher import Searcher

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Controller(Parent):

    def models(self):
        self.searchers = SearcherModel(self.config)

    def newsearch(self, msg, resp):
        sender = RPCSender(self.config)

        queue = sender.channel.queue_declare()
        queue_name = queue.method.queue

        results = self.searchers.mongoQuery({'QUERY': msg['data']['QUERY']})

        if len(results) > 0:
            searcher = results[0]

            sender.channel.queue_bind(
                exchange=searcher.OUTPUTEXCHANGE,
                queue=queue_name)

            req = sender.send_request(
                'SET',
                'hive',
                {'override': True},
                '',
                '',
                key=searcher.CONTROLQUEUE)
        else:
            searcher = self.searchers.new()
            r = sender.channel.queue_declare()
            q = r.method.queue
            machine = ProcHandler(
                self.config,
                Searcher(
                    self.config,
                    msg['data']['QUERY']),
                q)
            machine.start()

            req = json.loads(sender.send_request(
                'GET',
                'hive',
                {'variables': ['exchange']},
                '',
                '',
                key=q))

            searcher.OUTPUTEXCHANGE = req['exchange']
            searcher.CONTROLQUEUE = q
            searcher.QUERY = msg['data']['QUERY']

            sender.channel.queue_bind(
                exchange=searcher.OUTPUTEXCHANGE,
                queue=queue_name)

            req = sender.send_request(
                'SET',
                'hive',
                {'override': True},
                '',
                '',
                key=q)

            self.searchers.save(searcher)

        resp.respond({'queue': queue_name})

    def stop(self, msg, resp):
        searcher = self.searchers.find(msg.data)
        pub = SimplePublisher(
            ''. self.config['Rabbit']['host'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['passwords'])
        pub.publish_msg(self, 'STOP', searcher.CONTROLQUEUE)

        resp.respond('DELETED')

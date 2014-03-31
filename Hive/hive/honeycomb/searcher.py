import pika
from hive.common.longrunningproc import Proc
import time
import json
from hive.honeycomb.log import Log
from hive.common.model import ModelObject
from bson.objectid import ObjectId
import uuid

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Searcher(Proc):

    def __init__(self, config, query):
        Proc.__init__(self, config)
        self.connection = None
        self.channel = None
        self.exchange = None
        self.running = True
        self.query = query
        self.override = False
        self.previousids = set({}.keys())

    def getQueue(self):
        return self.queue

    def run(self):
        credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
        self.channel = self.connection.channel()

        # Setup queue for outputing data
        self.exchange = str(uuid.uuid4())
        self.channel.exchange_declare(exchange=self.exchange, type='fanout')

        logs = Log(self.config)

        self.ready.set()

        while self.running:
            results = logs.indexdriver.query(self.query)

            if results == {}:
                print "RECEIVED NO DATA SO DOING NOTHING -> CHECK HONEYCOMB, SIGNED Searcher"
            else:
                diff = set(results['hits'].keys()) - self.previousids

                if(len(diff) > 0) or self.override:
                    self.override = False
                    query = {'$or': []}
                    for hit in results['hits']:
                        query['$or'].append({logs.primary: ObjectId(hit)})

                    if len(results['hits']) > 0:
                        dbresult = logs.table.find(query)
                        for res in dbresult:
                            res['TIMESTAMP'] = str(res['_id'].generation_time)
                            res['_id'] = str(res['_id'])
                            results['hits'][str(res['_id'])]['log'] = ModelObject(
                                logs.columns, res).to_hash()

                        self.channel.basic_publish(
                            exchange=self.exchange,
                            routing_key='',
                            body=json.dumps(results))
                        self.previousids = set(results['hits'].keys())

            time.sleep(1)

        self.connection.close()

    def stop(self):
        running = False

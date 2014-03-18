import pika
from hive.common.longrunningproc import Proc
import time
import json
from hive.honeycomb.log import Log
from hive.common.model import ModelObject
from bson.objectid import ObjectId


class Searcher(Proc):

    def __init__(self, config, query):
        Proc.__init__(self, config)
        self.connection = None
        self.channel = None
        self.queue = None
        self.running = True
        self.query = query
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
        result = self.channel.queue_declare()
        self.queue = result.method.queue

        logs = Log(self.config)

        self.ready.set()

        while self.running:
            results = logs.indexdriver.query(self.query)
            diff = set(results['hits'].keys()) - self.previousids

            if(len(diff) > 0):
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
                        exchange='',
                        routing_key=self.queue,
                        body=json.dumps(results))
                    self.previousids = set(results['hits'].keys())

            time.sleep(1)

        self.connection.close()

    def stop(self):
        running = False

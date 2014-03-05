import pika
from hive.common.rpcsender import RPCSender
from hive.common.longrunningproc import Proc
import time
import json
import pika
from datetime import datetime
from hive.common.longrunningproc import Proc

class Alerter(Proc):

    def __init__(self, config, query, time, quantity):
        Proc.__init__(self, config)
        self.connection = None
        self.channel = None
        self.queue = None
        self.query = query
        self.maxTime = time
        self.maxQuantity = quantity
        self.capturedTime = time.time() + self.maxTime()
        self.currentCount = 0
        self.totalHits = 0
        self.query = query

    def run(self):
        # Connect to rabbit
        credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
        self.channel = self.connection.channel()

        # Setup queue for outputing data
        result = channel.queue_declare(exclusive=true)
        self.queue = result.method.queue

        # Push all historic data from honeycomb
        rpcSender = RPCSender(self.config, channel=self.channel)
        resp = rpcSender.send_request(
            'SEARCH',
            'honeycomb',
            json.dumps({ "QUERY": self.query }),
            '',
            'pheromonealerter',
            key='honeycomb')

        channel.basic_consume(on_message, queue=resp['data']['QUEUE'], no_ack=True)

        self.ready.set()

        channel.start_consuming()

    def on_message(self, channel, method_frame, header_frame, body):
        msg = json.loads(body)

        if((self.capturedTime + self.maxTime) < time.time()):
          self.capturedTime = time.time()
          self.currentCount = 0

        self.currentCount += (len(msg['data']['hits'] - self.totalHits))
        if(self.currentCount >= self.maxQuantity):
          if(self.totalHits != 0): 
            send_alert()
          self.capturedTime = time.time()
          self.currentCount = 0
          self.totalHits = len(msg['data']['hits'])

    def send_alert(self): 
        message = { "action":"ALERT", "to":"listener", "from":"pheromonealerter", "data": {}, "machineid":"something" }
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(message))

    def stop(self):
        self.connection.close()

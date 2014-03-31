import pika
from hive.common.rpcsender import RPCSender
from hive.common.longrunningproc import Proc
import time
import json
import pika
import uuid
from datetime import datetime
from hive.common.longrunningproc import Proc

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Alerter(Proc):

    def __init__(self, config, query, maxTime, quantity, message, user):
        Proc.__init__(self, config)
        self.connection = None
        self.channel = None
        self.uuid = str(uuid.uuid4())
        self.query = query
        self.message = message
        self.user = user
        self.maxTime = maxTime
        self.maxQuantity = quantity
        self.capturedTime = time.time() + self.maxTime
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

        # Setup recurring search
        rpcSender = RPCSender(self.config)
        resp = json.loads(rpcSender.send_request(
            'SEARCH',
            'honeycomb',
            {"QUERY": self.query, "TIMESCALE": 604800},
            '',
            'pheromonealerter',
            key='honeycomb'))

        self.channel.basic_consume(
            self.on_message,
            queue=resp['data']['queue'],
            no_ack=True)

        self.ready.set()

        self.channel.start_consuming()

    def on_message(self, channel, method_frame, header_frame, body):
        msg = json.loads(body)

        if((self.capturedTime + self.maxTime) < time.time()):
            self.capturedTime = time.time()
            self.currentCount = 0

        self.currentCount = self.currentCount + \
            (len(msg['hits']) - self.totalHits)
        if(self.currentCount >= self.maxQuantity):
            if(self.totalHits != 0):
                self.send_alert(self.currentCount)
            self.capturedTime = time.time()
            self.currentCount = 0

        self.totalHits = len(msg['hits'])

    def send_alert(self, count):
        print "FIRING AN EVENT!!!!!!"
        message = {
            "action": "EVENT",
            "to": "listener",
            "from": "pheromonealerter",
            "data": {"ALERT": {"UUID": self.uuid, "COUNT": count, "TEXT": self.message, 'USER': self.user}},
            "machineid": "something"}
        self.channel.basic_publish(
            exchange='apiary',
            routing_key="events.pheromone.alert",
            body=json.dumps(message))

    def stop(self):
        self.connection.close()

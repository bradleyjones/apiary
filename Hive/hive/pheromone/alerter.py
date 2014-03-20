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
        self.uuid = str(uuid.uuid4())
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

        # Setup recurring search
        rpcSender = RPCSender(self.config, channel=self.channel)
        resp = rpcSender.send_request(
            'SEARCH',
            'honeycomb',
            json.dumps({"QUERY": self.query}),
            '',
            'pheromonealerter',
            key='honeycomb')

        channel.basic_consume(
            on_message,
            queue=resp['data']['QUEUE'],
            no_ack=True)

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
                send_alert(self.currentCount)
            self.capturedTime = time.time()
            self.currentCount = 0
            self.totalHits = len(msg['data']['hits'])

    def send_alert(self, count):
        message = {
            "action": "EVENT",
            "to": "listener",
            "from": "pheromonealerter",
            "data": {"ALERT": { "COUNT": count, "TEXT": "Rate Exceeded!"}},
            "machineid": "something"}
        self.channel.basic_publish(
            exchange='apiary',
            routing_key="events.pheromone.alert",
            body=json.dumps(message))

    def stop(self):
        self.connection.close()

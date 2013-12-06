from multiprocessing import Process
import threading
import pika
from hive.common.rpcsender import RPCSender


class Machine(Process):

    def __init__(self, config):
        super(Machine, self).__init__()
        self.config = config
        self.connection = None
        self.channel = None
        self.stopqueue = None
        self.writer = None

    def run(self):
        #### Control Rig Setup ####
        credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
        self.channel = self.connection.channel()
        result = channel.queue_declare(exclusive=True)
        self.stopqueue = result.method.queue
        ############################

        self.writer = Writer(self.config)
        self.writer.start()

        # Start Consuming Stop Queue
        channel.basic_consume(on_message, queue=self.stopqueue, no_ack=True)
        channel.start_consuming()

    def on_message(self, channel, method_frame, header_frame, body):
        if body == "STOP":
            self.writer.stop()
            self.connection.close()


class Writer(threading.Thread):

    def __init__(self, config):
        super(Machine, self).__init__()
        self.daemon = True
        self.config = config
        self.connection = None
        self.channel = None
        self.queue = None

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
        rpcSender = RPCSender(self.config)
        resp = rpcSender.send_request(
            'THINGS',
            'honeycomb',
            '{}',
            'SOMETHING',
            'timemachineworker',
            key='honeycomb')
        for log in resp.data:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=log)

        # Start listening for live data to forward
        result = channel.queue_declare(exclusive=true)
        self.buff = result.method.queue
        channel.queue_bind(
            exchange='apiary',
            queue=self.buff,
            routing_key='agent.*.data')
        channel.basic_consume(on_message, queue=self.buff, no_ack=True)
        channel.start_consuming()

    def on_message(self, channel, method_frame, header_frame, body):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=log)

    def stop(self):
        self.connection.close()

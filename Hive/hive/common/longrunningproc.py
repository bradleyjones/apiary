import json
from multiprocessing import Process
import threading
import pika
from hive.common.rpcsender import RPCSender
import time


class ProcHandler(Process):

    def __init__(self, config, subproc, queue):
        Process.__init__(self)
        self.config = config
        self.connection = None
        self.channel = None
        self.stopqueue = queue
        self.subproc = subproc

    def run(self):
        #### Control Rig Setup ####
        credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
        self.channel = self.connection.channel()
        ############################

        self.subproc.start()

        if(not self.subproc.ready.wait(10)):
            raise Exception("Long running process failed to start")

        # Start Consuming Stop Queue
        self.channel.basic_consume(
            self.on_message,
            queue=self.stopqueue,
            no_ack=True)
        self.channel.start_consuming()

    def on_message(self, channel, method_frame, props, body):
        da = json.loads(body)
        if da['action'] == 'STOP':
            self.subproc.stop()
            self.connection.close()
        elif da['action'] == "SET":
            for var in da['data']:
                setattr(self.subproc, var, da['data'][var])
            self.channel.basic_publish(exchange='',
                                       routing_key=props.reply_to,
                                       properties=pika.BasicProperties(
                                           correlation_id=props.correlation_id,
                                       ),
                                       body={})
        elif da['action'] == "GET":
            response = {}
            for var in da['data']['variables']:
                response[var] = getattr(self.subproc, var)
            self.channel.basic_publish(exchange='',
                                       routing_key=props.reply_to,
                                       properties=pika.BasicProperties(
                                           correlation_id=props.correlation_id,
                                       ),
                                       body=json.dumps(response))


class Proc(threading.Thread):

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.daemon = True
        self.config = config
        self.ready = threading.Event()

    def run(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError

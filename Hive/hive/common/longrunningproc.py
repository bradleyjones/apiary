from multiprocessing import Process
import threading
import pika
from hive.common.rpcsender import RPCSender
import time

class ProcHandler(Process):

    def __init__(self, config, subproc):
        super(Machine, self).__init__()
        self.config = config
        self.connection = None
        self.channel = None
        self.stopqueue = None
        self.subproc = subproc
        self.ready = threading.Event()

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

        self.subproc.start()
        
        if(not subproc.ready.wait(10)) {
            raise Exception("Long Running Process Failed to Start")
        }
        self.ready.set()
      
        # Start Consuming Stop Queue
        channel.basic_consume(on_message, queue=self.stopqueue, no_ack=True)
        channel.start_consuming()

    def on_message(self, channel, method_frame, header_frame, body):
        if body == "STOP":
            self.subproc.stop()
            self.connection.close()

class Proc(threading.Thread):
    def __init__(self, config):
        self.daemon = True
        self.config = config
        self.ready = threading.Event()

    def run(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError

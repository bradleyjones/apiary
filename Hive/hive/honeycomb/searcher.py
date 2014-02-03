import pika
from hive.common.rpcsender import RPCSender
from hive.common.longrunningproc import Proc
import time

class Searcher(Proc):

    def __init__(self, config):
        super(Proc).__init__(config)
        self.connection = None
        self.channel = None
        self.queue = None
        self.running = True

    def run(self):
        credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
        self.channel = self.connection.channel()

        # Setup queue for outputing data
        result = channel.queue_declare(exclusive=true)
        self.queue = result.method.queue

        while self.running:
            ## TODO INSERT LUCENE SERACHING STUFF HERE
            searchresults = None
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=searchresults)
            time.sleep(1)
        
        self.connection.close()

    def stop(self):
        running = False

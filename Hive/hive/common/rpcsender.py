import pika
import uuid
import json
import time
import inspect
import threading

class RPCSender(object):

    def __init__(self, config, channel=None):
        self.config = config
        if channel is None:
            self.credentials = pika.PlainCredentials(
                self.config['Rabbit']['username'],
                self.config['Rabbit']['password'])
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.config['Rabbit']['host'], credentials=self.credentials))
            self.channel = self.connection.channel()
        else:
            self.channel = channel

        self.event = None
        self.corr_id = str(uuid.uuid4())
        self.resp = None
        self.id = "7beaecc1-d100-433b-803f-59920cc4dd20"

        if type(self.channel) is pika.channel.Channel:
          self.event = threading.Event()
          self.channel.queue_declare(self.onQueueOk, exclusive=True)
        elif type(self.channel) is pika.adapters.blocking_connection.BlockingChannel:
          self.result = self.channel.queue_declare(exclusive=True)
          self.callback_queue = self.result.method.queue
          self.channel.basic_consume(self.on_response, no_ack=True,
                                     queue=self.callback_queue)

    def onQueueOk(self, method_frame):
        print "Queue Created!"
        self.callback_queue = method_frame.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
        self.event.set()

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.resp = body

    def send_request(self, action, to, body, machineid,
                     fro, timeout=10, exchange='', key=''):
        if self.event is not None:
          self.event.wait()

        self.resp = None

        if not isinstance(body, dict):
            raise TypeError('Data must be a dict')

        data = {}
        data['action'] = action
        data['to'] = to
        data['from'] = fro
        data['data'] = body
        data['machineid'] = machineid

        self.channel.basic_publish(exchange=exchange,
                                   routing_key=key,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=json.dumps(data))
        starttime = time.time()
        while self.resp is None:
          if (starttime + timeout) <= time.time():
            return "Timeout!"
          self.connection.process_data_events()

        return self.resp

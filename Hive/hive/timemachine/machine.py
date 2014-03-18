import pika
from hive.common.rpcsender import RPCSender
from hive.common.longrunningproc import Proc


class Writer(Proc):

    def __init__(self, config):
        super(Proc).__init__(config)
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

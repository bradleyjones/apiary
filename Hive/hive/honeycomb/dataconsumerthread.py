import threading

class DataConsumerThread(threading.Thread):

    def __init__(self), config):
        self.config = config
        self.credentials = pika.PlainCredentials(self.config['Rabbit']['username'], self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=self.credentials))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='apiary',
                                         type='topic')
        self.result = channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='apiary',
                       queue=queue_name,
                       routing_key="data")
        self.channel.basic_consume(on_message, queue=self.queue_name, no_ack=True)

    def run(self):
        self.channel.start_consuming() 

    def stop(self):
        self.channel.stop_consuming()
        connection.close()

    def on_message(self, chan, method, head, body):
        print body

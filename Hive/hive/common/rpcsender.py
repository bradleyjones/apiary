import pika


class RPCSender(object):

  def __init__(self, config):
      self.credentials = pika.PlainCredentials(
          self.config['Rabbit']['username'],
          self.config['Rabbit']['password'])
      self.connection = pika.BlockingConnection(pika.ConnectionParameters(
          host=self.config['Rabbit']['host'], credentials=self.credentials))
      self.channel = self.connection.channel()
      self.corr_id = str(uuid.uuid4())
      self.resp = None
      self.id = "7beaecc1-d100-433b-803f-59920cc4dd20" 
      self.result = self.channel.queue_declare(exclusive=True)
      self.callback_queue = result.method.queue
      self.channel.basic_consume(self.on_response, no_ack=True,
                                 queue=self.callback_queue)

  def on_response(self, ch, method, props, body):
      if self.corr_id == props.correlation_id:
          self.resp = body

  def send_request(self, action, to, data, exchange='', key=''):
      self.resp = None

      data = {}
      data['action'] = "INSERT"
      data['to'] = "hive"
      data['from'] = self.id
      data['data'] = json.dumps(data)
      data['machineid'] = "havsbdjhlbasd"

      self.channel.basic_publish(exchange=exchange,
                            routing_key=key,
                            properties=pika.BasicProperties(
                                reply_to=callback_queue,
                                correlation_id=self.corr_id,
                            ),
                            body=json.dumps(data))
      
      while self.resp is None:
          self.connection.process_data_events()

      return self.resp
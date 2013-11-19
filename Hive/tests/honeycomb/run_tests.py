import uuid
import pika
import json
import unittest
from configobj import ConfigObj, ConfigObjError


def loadConfig(filepath):
    try:
        return ConfigObj(filepath, file_error=True)
    except (ConfigObjError, IOError) as e:
        logging.error("Config File Doesn't Exist: %s", filepath)
        raise SystemExit


class HoneycombBasicTest(unittest.TestCase):

    def setUp(self):
        self.config = loadConfig('config.ini')

        self.credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config['Rabbit']['host'], credentials=self.credentials))
        self.channel = self.connection.channel()
        self.corr_id = str(uuid.uuid4())
        self.resp = None
        self.id = "7beaecc1-d100-433b-803f-59920cc4dd20" 

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.resp = body


class HoneycombTestInsert(HoneycombBasicTest):
    def runTest(self):
        result = self.channel.queue_declare(exclusive=True)
        callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=callback_queue)

        data = {}
        data['action'] = "INSERT"
        data['to'] = "hive"
        data['from'] = self.id
        data['data'] = '{ "Time":12334231, "Text":"TESTESTESTESTEST" }'
        data['machineid'] = "havsbdjhlbasd"
        self.channel.basic_publish(exchange='',
                              routing_key='honeycomb',
                              properties=pika.BasicProperties(
                                  reply_to=callback_queue,
                                  correlation_id=self.corr_id,
                              ),
                              body=json.dumps(data))
        while self.resp is None:
            self.connection.process_data_events()

        self.result = json.loads(self.resp)
        self.assertTrue(self.result['data'] == 'OK')
        self.assertTrue(self.result['from'] == 'honeycomb')
        self.assertTrue(self.result['to'] == self.id)

class HoneycombTestFind(HoneycombBasicTest):
    def runTest(self):
        result = self.channel.queue_declare(exclusive=True)
        callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=callback_queue)

        data = {}
        data['action'] = "FIND"
        data['to'] = "hive"
        data['from'] = self.id
        data['data'] = '{ "Time":12334231 }'
        data['machineid'] = "havsbdjhlbasd"
        self.channel.basic_publish(exchange='',
                              routing_key='honeycomb',
                              properties=pika.BasicProperties(
                                  reply_to=callback_queue,
                                  correlation_id=self.corr_id,
                              ),
                              body=json.dumps(data))
        while self.resp is None:
            self.connection.process_data_events()

        self.result = json.loads(self.resp)
        self.assertTrue(self.result['data'][0]['Time']  == 12334231)
        self.assertTrue(self.result['from'] == 'honeycomb')
        self.assertTrue(self.result['to'] == self.id)

honeycombTestSuite = unittest.TestSuite()
honeycombTestSuite.addTest(HoneycombTestInsert('runTest'))
honeycombTestSuite.addTest(HoneycombTestFind('runTest'))

unittest.TextTestRunner(verbosity=2).run(honeycombTestSuite)

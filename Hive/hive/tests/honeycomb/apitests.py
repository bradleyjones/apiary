import json
import unittest
import pika
from hive.tests.basictest import HiveBasicTest


class HoneycombApiTests(HiveBasicTest):

    def testInsert(self):
        result = self.channel.queue_declare(exclusive=True)
        callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=callback_queue)

        data = {}
        data['action'] = "INSERT"
        data['to'] = "hive"
        data['from'] = self.id
        data['data'] = {"Time": 1234567, "Text": "TESTESTESTESTEST"}
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

    def testFind(self):
        result = self.channel.queue_declare(exclusive=True)
        callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=callback_queue)

        data = {}
        data['action'] = "FIND"
        data['to'] = "hive"
        data['from'] = self.id
        data['data'] = {"Time": 1234567}
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
        self.assertTrue(self.result['data'][0]['Time'] == 1234567)
        self.assertTrue(self.result['from'] == 'honeycomb')
        self.assertTrue(self.result['to'] == self.id)

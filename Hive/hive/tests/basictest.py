import uuid
import pika
import json
import unittest
import logging
from configobj import ConfigObj, ConfigObjError


def loadConfig(filepath):
    try:
        return ConfigObj(filepath, file_error=True)
    except (ConfigObjError, IOError) as e:
        logging.error("Config File Doesn't Exist: %s", filepath)
        raise SystemExit


class HiveBasicTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(HiveBasicTest, self).__init__(*args)
        self.configname = kwargs.get('configname', "")

    def setUp(self):
        self.config = loadConfig('%s_config.ini' % self.configname)

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

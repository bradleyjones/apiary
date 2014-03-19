import uuid
import random
import json
from simplepublisher import SimplePublisher
import logging


class Controller(object):

    def __init__(self, config, channel):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.channel = channel
        self.models()
        self.publisher = SimplePublisher(
            'apiary',
            channel=channel)

    def models(self):
        pass

    def event(self, data, key=None):
        rk = "events.%s" % self.config['Rabbit']['event_prefix']
        if key is not None:
            rk = "%s.%s" % (rk, key)
        doc = {
            'action': 'EVENT',
            "to": "hive",
            "from": "hive",
            "data": data,
            "machineid": "boop"}
        self.publisher.publish_msg(json.dumps(doc), rk)

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

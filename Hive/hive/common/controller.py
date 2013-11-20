import uuid
import random
import json
from simplepublisher import SimplePublisher
import logging


class Controller(object):

    def __init__(self, config):
        self.config = config
        self.models()
        self.logger = logging.getLogger(__name__)
        self.publisher = SimplePublisher(
            'apiary',
            self.config['Rabbit']['host'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

    def models(self):
        pass

    def event(self, data, key=None):
        rk = "events.%s" % self.config['Rabbit']['event_prefix']
        if key is not None:
          rk = "%s.%s" % (rk, key)
        self.publisher.publish_msg(data, rk)

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

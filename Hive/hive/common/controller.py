import uuid
import random
import json
from pubsubserver import PubSubServer
import logging


class Controller(object):

    def __init__(self, config):
        self.config = config
        self.models()
        self.logger = logging.getLogger(__name__)
        self.pubsub = PubSubServer(
            'events',
            self.config['Rabbit']['host'],
            self.config['Rabbit']['event_prefix'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

    def models(self):
        pass

    def event(self, data, key=None):
        self.pubsub.publish_msg(data, key)

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

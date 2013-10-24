import uuid
import random
import json
from pubsubserver import PubSubServer
import logging


class Controller(object):

    def __init__(self, config):
        self.agents = {}
        self.config = config
        self.extra_data()
        self.logger = logging.getLogger(__name__)

    def extra_data(self):
        pass

    def run(self):
        self.pubsub = PubSubServer(
            'events',
            self.config['Base']['rabbit_ip'],
            self.config['Base']['event_prefix'])

    def event(self, data, key=None):
        self.pubsub.publish_msg(data, key)

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

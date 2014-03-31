import uuid
import random
import json
from simplepublisher import SimplePublisher
import logging

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Controller(object):

    """Parent class to all controllers in the apiary project, provides basic
    setup such as logging and a simple publisher."""

    def __init__(self, config, channel):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.channel = channel
        self.models()
        self.publisher = SimplePublisher(
            'apiary',
            channel=channel)

    def models(self):
        """Called from the constructor so it provides a known interface for
        extended controllers to place their model code."""
        pass

    def event(self, data, key=None):
        """This provides a method for sending events out on to the message
        bus."""
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
        """A default and example controller action."""
        resp.respond("THIS IS THE DEFAULT ACTION")

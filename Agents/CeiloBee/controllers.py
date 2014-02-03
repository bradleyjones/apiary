import uuid
import random
import json
import threading
import time
import keystoneclient.v2_0.client as ksclient
import ceilometerclient import celioclient
from hive.common.controller import Controller as Parent
from hive.common.simplepublisher import SimplePublisher
from openstack import Openstack
from uuid import getnode as get_mac


class Controller(Parent):

    def models(self):
        self.openstacks = Openstack(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def handshake(self, data, resp):

        class HeartBeater(threading.Thread):
            def __init__(self, clientID, heartbeatInterval):
                self.clientID = clientID
                self.heartbeatInterval = heartbeatInterval

            def run(self):
                while(1):
                   time.sleep(self.heartbeatInterval)
                   self.logger.debug("Sending HeartBeat")
                   message = {
                       "action": "HEARTBEAT"
                       "to": "AgentManager"
                       "from": self.clientID
                       "data": "Beat"
                       "machineID": get_mac()
                   }
                   self.publisher.publish(message,"agents"+self.clientID+".heartbeat")

        self.clientID = data.UUID
        self.heartbeater = HeartBeater(self.clientID, self.config['Agent']['heartbeatInterval'])
        self.heartbeater.start()
        self.logger.debug("Agent Initialised")

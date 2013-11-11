from uuid import getnode as get_mac
import pika
import logging
import time
import threading
from agent import Agent
import json


class HeartbeatThread(threading.Thread):

    def __init__(self, config):
        super(HeartbeatThread, self).__init__()
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.daemon = True
        self.host = self.config['Rabbit']['host']
        self.credentials = pika.PlainCredentials(
            config['Rabbit']['username'],
            config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=self.credentials))
        self.channel = self.connection.channel()
        self.logger = logging.getLogger(__name__)
        self.machineid = str(get_mac())

    def run(self):
        self.agentmodel = Agent(self.config)
        while(True):
            agents = self.agentmodel.findAll()
            time.sleep(30)
            self.logger.info("Heartbeating...")
            for key, agent in agents.iteritems():
                if (agent.HEARTBEAT + 20) < time.time():
                    if not agent.DEAD:
                        event = {}
                        event[agent.UUID] = agent.to_hash()
                        self.channel.basic_publish('',
                                                   agent.QUEUE,
                                                   self.makeMessage(
                                                       agent.UUID),
                                                   pika.BasicProperties(
                                                       content_type='text/plain',
                                                       delivery_mode=1,
                                                       reply_to='control'))

    def makeMessage(self, to):
        response = {}
        response['action'] = "HEARTBEAT"
        response['to'] = to
        response['from'] = "control"
        response['data'] = ""
        response['machineid'] = self.machineid
        return json.dumps(response)

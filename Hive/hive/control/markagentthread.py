from agent import Agent
import time
from ..common.pubsubserver import PubSubServer
import threading 
import logging
import json

class MarkAgentsThread(threading.Thread): 

    def __init__(self, config):
        super(MarkAgentsThread, self).__init__()
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.daemon = True

    def run(self):
        self.pubsub = PubSubServer(
            'events',
            self.config['Rabbit']['host'],
            self.config['Rabbit']['event_prefix'])
        agentmodel = Agent(self.config)
        while(True):
            agents = agentmodel.findAll()
            time.sleep(30)
            self.logger.info("Scanning for Dead Agents...")
            for key, agent in agents.iteritems():
                if (agent.HEARTBEAT + 300) < time.time():
                    if not agent.DEAD:
                        agent.DEAD = True
                        self.logger.info("Agent %s is Dead!", agent.UUID)
                        event = {}
                        event[agent.UUID] = agent.to_hash()
                        self.pubsub.publish_msg(json.dumps(event), 'agents')
                        agentmodel.save(agent)

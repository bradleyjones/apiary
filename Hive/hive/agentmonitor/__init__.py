"""Apiary component used for monitoring the heartbeats of Agents looked after
by the Agent Manager, will mark Agents as dead if they havn't been heard from
in 5 minutes."""

import time
import threading
import logging
import json
import sys
import pika
from configobj import ConfigObj, ConfigObjError
from hive.common.simplepublisher import SimplePublisher
from hive.common.base import Base
from hive.agentmanager.agent import Agent

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class AgentMonitor(Base):

    def __init__(self):
        super(AgentMonitor, self).__init__('agentmanager')
        self.publisher = SimplePublisher(
            'apiary',
            self.config['Rabbit']['host'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

    def start(self):
        try:
            self.agentmodel = Agent(self.config)

            while(True):
                self.logger.debug("Scanning agents...")
                agents = self.agentmodel.findAll()
                for agent in agents:
                    # Scan for Dead Agents
                    if ((agent.HEARTBEAT + 300) < time.time()) and (not agent.DEAD):
                        agent.DEAD = True
                        self.logger.info("Agent %s is Dead!", agent.UUID)
                        event = {}
                        event[agent.UUID] = agent.to_hash()

                        doc = {
                            'action': 'EVENT',
                            "to": "hive",
                            "from": "hive",
                            "data": {'agents': event},
                            "machineid": "boop"}
                        self.publisher.publish_msg(
                            json.dumps(doc),
                            'events.agentmanager.agent.dead')
                        self.agentmodel.save(agent)

                # Added sleep for the CPU's sake
                time.sleep(1)

        except Exception as e:
            self.logger.error("Errors Occured: %s", str(e))
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.logger.info("Exiting...")
            sys.exit(0)

    def stop(self):
        pass


def main():
    agentmonitor = AgentMonitor()
    agentmonitor.start()

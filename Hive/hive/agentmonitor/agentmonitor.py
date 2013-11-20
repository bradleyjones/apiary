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
                for key, agent in agents.iteritems():
                    # Scan for Dead Agents
                    if ((agent.HEARTBEAT + 300) < time.time()) and (not agent.DEAD):
                        agent.DEAD = True
                        self.logger.info("Agent %s is Dead!", agent.UUID)
                        event = {}
                        event[agent.UUID] = agent.to_hash()
                        self.publisher.publish_msg(json.dumps(event), 'events.agentmanager.agent.dead')
                        self.agentmodel.save(agent)

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

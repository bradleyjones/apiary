import time
from ..common.pubsubserver import PubSubServer
from configobj import ConfigObj, ConfigObjError
from ..common.base import Base
from ..control.agent import Agent
import threading
import logging
import json
import sys


class ControlMarker(Base):

    def __init__(self):
        super(ControlMarker, self).__init__('control')
        self.pubsub = PubSubServer(
            'events',
            self.config['Rabbit']['host'],
            self.config['Rabbit']['event_prefix'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

    def loadConfig(self, filepath):
        try:
            return ConfigObj(filepath, file_error=True)
        except (ConfigObjError, IOError) as e:
            logging.error("Config File Doesn't Exist: %s", filepath)
            raise SystemExit

    def start(self):
        try:
            self.agentmodel = Agent(self.config)
            while(True):
                agents = self.agentmodel.findAll()
                time.sleep(30)
                self.logger.debug("Scanning for Dead Agents...")
                for key, agent in agents.iteritems():
                    if ((agent.HEARTBEAT + 300) < time.time()) and (not agent.DEAD):
                        agent.DEAD = True
                        self.logger.info("Agent %s is Dead!", agent.UUID)
                        event = {}
                        event[agent.UUID] = agent.to_hash()
                        self.pubsub.publish_msg(json.dumps(event), 'agents')
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
    controlmarker = ControlMarker()
    controlmarker.start()

import time
from ..common.pubsubserver import PubSubServer
from configobj import ConfigObj, ConfigObjError
from ..common.base import Base
from ..control.agent import Agent
import threading
import logging
import json
import sys
import pika


class ControlMarker(Base):

    def __init__(self):
        super(ControlMarker, self).__init__('control')
        self.config = self.loadConfig('control_config.ini')
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

            credentials = pika.PlainCredentials(
                self.config['Rabbit']['username'],
                self.config['Rabbit']['password'])
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
            channel = connection.channel()

            channel.exchange_declare(exchange='apiary',
                                     type='topic')

            channel.queue_declare(
                queue=self.config['Rabbit']['sub_queue'],
                durable=True)

            while(True):
                self.logger.info("Scanning agents...")
                agents = self.agentmodel.findAll()
                for key, agent in agents.iteritems():
                    # Scan for Dead Agents
                    if ((agent.HEARTBEAT + 300) < time.time()) and (not agent.DEAD):
                        agent.DEAD = True
                        self.logger.info("Agent %s is Dead!", agent.UUID)
                        event = {}
                        event[agent.UUID] = agent.to_hash()
                        self.pubsub.publish_msg(json.dumps(event), 'agents')
                        self.agentmodel.save(agent)
                    # Bind Control Data Queue
                    if (not agent.DEAD) and (agent.AUTHENTICATED):
                        self.logger.info(
                            "Binding Control Data to %s" %
                            agent.UUID)
                        channel.queue_bind(exchange='apiary',
                                           queue=self.config[
                                               'Rabbit'][
                                               'sub_queue'],
                                           routing_key='data.%s' % agent.UUID)
                time.sleep(30)
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

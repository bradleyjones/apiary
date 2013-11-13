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


class ControlStateMachine(Base):

    def __init__(self):
        super(ControlStateMachine, self).__init__('control')
        self.pubsub = PubSubServer(
            'events',
            self.config['Rabbit']['host'],
            self.config['Rabbit']['event_prefix'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

    def start(self):
        try:
            self.agentmodel = Agent(self.config)

            credentials = pika.PlainCredentials(
                self.config['Rabbit']['username'],
                self.config['Rabbit']['password'])
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.config['Rabbit']['host'], credentials=credentials))
    
            self.logger.info("Connected!")

            channel = connection.channel()

            channel.exchange_declare(exchange='apiary',
                                     type='topic')

            channel.queue_declare(
                queue=self.config['Rabbit']['sub_queue'],
                durable=True)

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
                        self.pubsub.publish_msg(json.dumps(event), 'agents')
                        self.agentmodel.save(agent)
                    # Bind Control Data Queue
                    if (not agent.DEAD) and (agent.AUTHENTICATED) and (not agent.BOUND):
                        self.logger.info(
                            "Binding Control Data to %s" %
                            agent.UUID)
                        channel.queue_bind(exchange='apiary',
                                           queue=self.config[
                                               'Rabbit'][
                                               'sub_queue'],
                                           routing_key='data.%s' % agent.UUID)
                        agent.BOUND = True
                        self.agentmodel.save(agent)
                    elif (not agent.DEAD) and (not agent.AUTHENTICATED) and (agent.BOUND):
                        self.logger.info(
                            "Unbinding Control Data to %s" %
                            agent.UUID)
                        channel.queue_unbind(exchange='apiary',
                                           queue=self.config[
                                               'Rabbit'][
                                               'sub_queue'],
                                           routing_key='data.%s' % agent.UUID)
                        agent.BOUND = False
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
    controlstate = ControlStateMachine()
    controlstate.start()

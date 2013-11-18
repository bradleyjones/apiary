import time
from ..common.pubsubserver import PubSubServer
from configobj import ConfigObj, ConfigObjError
from ..common.base import Base
from ..honeycomb.subscription import Subscription
import threading
import logging
import json
import sys
import pika


class HoneycombStateMachine(Base):

    def __init__(self):
        super(HoneycombStateMachine, self).__init__('honeycomb')
        self.pubsub = PubSubServer(
            'events',
            self.config['Rabbit']['host'],
            self.config['Rabbit']['event_prefix'],
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

    def start(self):
        try:
            self.subs = Subscription(self.config)

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
                self.logger.debug("Scanning subs...")
                subscriptions = self.subs.findAll()
                for key, sub in subscriptions.iteritems():
                    # Bind Control Data Queue
                    if (sub.AUTHENTICATED) and (not agent.BOUND):
                        self.logger.info(
                            "Binding Control Data to %s" %
                            sub.UUID)
                        channel.queue_bind(exchange='apiary',
                                           queue=self.config[
                                               'Rabbit'][
                                               'sub_queue'],
                                           routing_key='data.%s' % sub.UUID)
                        sub.BOUND = True
                        self.submodel.save(agent)
                    elif (not sub.AUTHENTICATED) and (agent.BOUND):
                        self.logger.info(
                            "Unbinding Control Data to %s" %
                            sub.UUID)
                        channel.queue_unbind(exchange='apiary',
                                           queue=self.config[
                                               'Rabbit'][
                                               'sub_queue'],
                                           routing_key='data.%s' % sub.UUID)
                        sub.BOUND = False
                        self.submodel.save(agent)
                        
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
    honeystate = HoneycombStateMachine()
    honeystate.start()

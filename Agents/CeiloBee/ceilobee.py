#!/usr/bin/env python
from routes import Routes
from configobj import ConfigObj, ConfigObjError
import pika
import uuid
import json
import time
import logging
from uuid import getnode as get_mac
from hive.common.rpcresponse import RPCResponse

class CeiloBee():

    def __init__(self):
        name = "ceilobee"
        self.config = self.loadConfig("/etc/apiary/%s_config.ini" % name)
        self.configureLogger(
            self.config['Logging']['location'],
            self.config['Logging']['level'])
        self.logger = logging.getLogger(__name__)


    def start(self, r):
        # Set Router
        self.router = r(self.config)
        
        # Set Logger
        self.logger.info(
            "CelioBEE is starting on Rabbit %s" %
            self.config['Rabbit']['host'])

        #Initialise Rabbit conneciton, blank queue
        self.credentials = pika.PlainCredentials(
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config['Rabbit']['host'], credentials=self.credentials))
        self.channel = self.connection.channel()
        self.corr_id = str(uuid.uuid4())
        self.id = "Unidentified"
        self.result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = self.result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=False, queue=self.callback_queue)

        self.alertHive()

    # On response, send to router.
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            
            request = {}
            rpcresp = RPCResponse()
            response = "INVALID MESSAGE RECEIVED"

            try:
                request = self.jsonToHash(body)
                self.logger.info('Message Receieved: %s', str(request))
                request['reply_to'] = props.reply_to

                try:
                    self.router(request["action"], request, rpcresp)
                except Exception as e:
                    rpcresp.action = "Error"
                    rpcresp.data = traceback.format_exc()
                    self.logger.error('Inner Error Occured: %s', rpcresp.data)
            except Exception as e:
                rpcresp.action = "Error"
                rpcresp.data = traceback.format_exc()
                request['from'] = "Unknown"
                self.logger.error(
                    'Outer Error Occured: %s',
                    traceback,format_exc())
             
    # Give Hive credentials
    def alertHive(self):
        
        # Build Payload
        data = {}
        data['action'] = "HANDSHAKE"
        data['to'] = "AgentManager"
        data['from'] = "Undefined"
        data['data'] = {}
        data['machineID'] = get_mac()

        # Send
        self.channel.basic_publish(exchange='',routing_key='',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=json.dumps(data))
    
    def loadConfig(self, filepath):
        try:
            return ConfigObj(filepath, file_error=True)
        except (ConfigObjError, IOError) as e:
            logging.error("Config File Doesn't Exist: %s", filepath)
            raise SystemExit

    def configureLogger(self, filelocation, level):
        if level == "debug":
            logging.basicConfig(filename=filelocation,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=logging.DEBUG)
        elif level == "info":
            logging.basicConfig(filename=filelocation,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=logging.INFO)
        elif level == "warning":
            logging.basicConfig(filename=filelocation,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=logging.WARNING)
        elif level == "error":
            logging.basicConfig(filename=filelocation,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=logging.ERROR)
        elif level == "critical":
            logging.basicConfig(filename=filelocation,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=logging.CRITICAL)
        else:
            raise Exception("Invalid Debug Level " + level)

        # create console handler and set level to debug
        logger = logging.getLogger()
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        # add formatter to ch
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        logging.info('Logging Beginning')

def main():
    ceiloagent = CeiloBee()
    ceiloagent.start(Routes)

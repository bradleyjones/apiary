"""This module contains Base, a underlying class for most hive components,
pulls in config file and setups up rabbit consumer and rabbit subscriber
threads."""

import logging
import sys
import time
import signal
from configobj import ConfigObj, ConfigObjError
from .rabbitconsumer import RabbitConsumer
from .rabbitsubscriber import RabbitSubscriber

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Base(object):

    """A common base class for most hive components, pulls in config file and
    setups up rabbit consumer and rabbit subscriber threads."""

    def __init__(self, name):
        self.config = self.loadConfig("/etc/apiary/%s_config.ini" % name)
        self.configureLogger(
            self.config['Logging']['location'],
            self.config['Logging']['level'])
        self.logger = logging.getLogger(__name__)

    def start(self, r):
        """Start the threads for receiving messages."""

        #: Initialise the controllers and router
        self.router = r(self.config)

        self.logger.info(
            "Setting Up Server on %s" %
            self.config['Rabbit']['host'])

        #: Create the RPC consumer
        self.rpc = RabbitConsumer(
            self.config['Rabbit']['rpc_queue'],
            self.config['Rabbit']['host'],
            self.router.route,
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

        #: Create the RPC subscriber
        self.subscriber = RabbitSubscriber(
            self.config['Rabbit']['sub_queue'],
            self.config['Rabbit']['host'],
            self.router.route,
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'],
            self.config['Rabbit']['sub_keys'])

        try:
            #: Start Threads
            self.extraThreads()
            time.sleep(1)
            self.rpc.start()
            time.sleep(1)
            self.subscriber.start()

            signal.signal(signal.SIGINT, self.han)

            while self.rpc.isAlive():
                self.rpc.join(600)

        except Exception as e:
            self.logger.error("Errors Occured: %s", str(e))
            self.rpc.stop()
            time.sleep(1)
            self.subscriber.stop()
        except (KeyboardInterrupt, SystemExit):
            self.rpc.stop()
            time.sleep(1)
            self.subscriber.stop()
        finally:
            self.logger.info("Exiting...")
            sys.exit(0)

    def han(self, signal, frame):
        self.rpc.stop()
        time.sleep(1)
        self.subscriber.stop()
        self.logger.info("Exiting...")
        sys.exit(0)

    def extraThreads(self):
        """Function that will get called inside the start function for any
        threads added in child classes."""
        pass

    def loadConfig(self, filepath):
        """Try to load config using ConfigObj and make sure it exists."""
        try:
            return ConfigObj(filepath, file_error=True)
        except (ConfigObjError, IOError) as e:
            logging.error("Config File Doesn't Exist: %s", filepath)
            raise SystemExit

    def configureLogger(self, filelocation, level):
        """Configure the logger format and logging level according to the
        config file."""

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

        #: Create console handler and set level to debug
        logger = logging.getLogger()
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        #: Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #: Add formatter to console handler
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        logging.info('Logging Beginning')

import logging
from configobj import ConfigObj, ConfigObjError
from rabbitconsumer import RabbitConsumer
from rabbitsubscriber import RabbitSubscriber
import sys
import time

class Base(object):

    def __init__(self, name):
        self.config = self.loadConfig("/etc/apiary/%s_config.ini" % name)
        self.configureLogger(
            self.config['Logging']['location'],
            self.config['Logging']['level'])
        self.logger = logging.getLogger(__name__)

    def start(self, r):
        # Initialise the controllers and router
        self.router = r(self.config)

        self.logger.info(
            "Setting Up Server on %s" %
            self.config['Rabbit']['host'])

        # Create the RPC consumer and data subscribers
        self.rpc = RabbitConsumer(
            self.config['Rabbit']['rpc_queue'],
            self.config['Rabbit']['host'],
            self.router.route,
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

        self.subscriber = RabbitSubscriber(
            self.config['Rabbit']['sub_queue'],
            self.config['Rabbit']['host'],
            self.router.route,
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])

        try:
            # Threads
            self.extraThreads()
            time.sleep(1)
            self.rpc.start()
            time.sleep(1)
            self.subscriber.start()

            while self.rpc.isAlive() and self.subscriber.isAlive():
                time.sleep(1)

        except Exception as e:
            self.logger.error("Errors Occured: %s", str(e))
            self.rpc.stop()
            time.sleep(1)
            self.subscriber.stop()
        except KeyboardInterrupt:
            self.rpc.stop()
            time.sleep(1)
            self.subscriber.stop()
        finally:
            self.logger.info("Exiting...")
            sys.exit(0)

    def extraThreads(self):
        pass

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

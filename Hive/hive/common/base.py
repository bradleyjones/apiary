import logging
from configobj import ConfigObj, ConfigObjError
from rpcserver import RPCServer
import sys

class Base(object):

    def __init__(self, name):
        self.config = self.loadConfig(name + "_config.ini")
        self.configureLogger(
            self.config['Logging']['location'],
            self.config['Logging']['level'])
        self.logger = logging.getLogger(__name__)
        self.cont = None
        self.router = None
        self.server = None

    def start(self, r, c):
        self.cont = c.Controller(self.config)
        self.router = r.Routes(self.cont)
        self.logger.info(
            "Setting Up Server on %s" %
            self.config['Rabbit']['host'])
        self.server = RPCServer(
            self.config['Rabbit']['queue_name'],
            self.config['Rabbit']['host'],
            self.router.route,
            self.config['Rabbit']['username'],
            self.config['Rabbit']['password'])
        try:
            self.extraThreads()
            self.cont.run()
            self.server.run()
        except Exception as e:
            self.logger.error("Errors Occured: %s", str(e))
        except KeyboardInterrupt:
            self.server.stop()
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

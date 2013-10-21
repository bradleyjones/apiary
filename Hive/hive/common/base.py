import logging
from configobj import ConfigObj, ConfigObjError
from rpcserver import RPCServer


class Base(object):

    def __init__(self, name):
        self.config = self.loadConfig(name + "_config.ini")
        self.configureLogger(
            self.config['Logging']['location'],
            self.config['Logging']['level'])
        self.logger = logging.getLogger(__name__)

    def startServer(self, r, c):
        cont = c.Controller()
        router = r.Routes(cont)
        self.logger.info(
            "Setting Up Server on %s" %
            self.config['Base']['rabbit_ip'])
        try:
            server = RPCServer(
                self.config['Base']['queue_name'],
                self.config['Base']['rabbit_ip'],
                router.route)
        except KeyboardInterrupt:
            self.logger.info("Exiting...")

    def loadConfig(self, filepath):
        try:
            return ConfigObj(filepath, file_error=True)
        except (ConfigObjError, IOError), e:
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

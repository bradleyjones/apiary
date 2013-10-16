import logging


class Controller(object):

    def default(self, data):
        logging.info("Data Received to default controller action: %s", data)
        return "THIS IS THE DEFAULT ACTION"

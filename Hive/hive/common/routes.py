import logging
import sys


class Routes(object):

    def __init__(self, config):
        self.routes = {}
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.setupRoutes()
        self.logger.info("Routes Loaded: " + str(self.routes.keys()))

    def setupRoutes(self):
        raise NotImplementedError()
    
    def my_import(self, name):
        __import__(name)
        return sys.modules[name]

    def route(self, action, data, resp):
        getattr(self, "invert_op", None)
        if action not in self.routes:
            raise RoutingException("Route not found for: " + action)
        else:
            cont = self.my_import(self.routes[action][1]).Controller(self.config)
            method = getattr(cont, self.routes[action][0], None)
            if not callable(method):
                raise RoutingException(
                    "Action not found in controller: " + str(self.routes[action]))
            else:
                self.logger.info(
                    "Route %s calling function %s",
                    action,
                    self.routes[action])
                method(data, resp)

    def action(self, name, func, controller):
        if name in self.routes:
            raise RoutingException("Route already exists: " + name)
        else:
            self.routes[name] = (func, controller)


class RoutingException(Exception):
    pass

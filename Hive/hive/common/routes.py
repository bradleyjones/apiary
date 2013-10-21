import logging


class Routes(object):

    def __init__(self, controller):
        self.routes = {}
        self.controller = controller
        self.logger = logging.getLogger(__name__)
        self.setupRoutes()
        self.logger.info("Routes Loaded: " + str(self.routes.keys()))

    def setupRoutes(self):
        return

    def route(self, action, data, resp):
        getattr(self, "invert_op", None)
        if action not in self.routes:
            raise RoutingException("Route not found for: " + action)
        else:
            method = getattr(self.controller, self.routes[action], None)
            if not callable(method):
                raise RoutingException(
                    "Action not found in controller: " + str(self.routes[action]))
            else:
                self.logger.info(
                    "Route %s calling function %s",
                    action,
                    self.routes[action])
                method(data, resp)

    def action(self, name, func):
        if name in self.routes:
            raise RoutingException("Route already exists: " + name)
        else:
            self.routes[name] = func


class RoutingException(Exception):
    pass

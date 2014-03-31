"""This module contains a wrapper class for RPC Responses in controllers."""

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class RPCResponse(object):

    """Wrapper class for RPC responses, it only allows for one call to respond
    to protect the user from overriding his own data."""

    def __init__(self):
        self.action = "DONE"
        self.data = ""
        self.responsemade = False

    def respond(self, data, action=None):
        if not self.responsemade:
            self.data = data
            if action is not None:
                self.action = action
            self.responsemade = True
        else:
            raise RPCResponseException("Multiple Calls to Respond Made")


class RPCResponseException(Exception):
    pass

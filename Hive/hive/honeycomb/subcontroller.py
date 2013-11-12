import logging


class Controller(object):

    def get(self, data, resp):
        resp.response("GET STUFF!")

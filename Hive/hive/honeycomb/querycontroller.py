"""Controller for more advanced and specfic query Actions."""

from pymongo import MongoClient
from ..common.controller import Controller as Parent
from hive.common.rpcsender import RPCSender
import json
from bson.objectid import ObjectId
from log import Log
import csv

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Controller(Parent):

    def models(self):
        self.logs = Log(self.config)

    def timestamps(self, msg, resp):
        logs = self.logs.mongoQuery({}, {'EVENTTIMESTAMP': 1})
        response = {}
        for log in logs:
            response[str(log._id)] = log.to_hash()
        resp.respond(response)

    def tags(self, msg, resp):
        logs = self.logs.mongoQuery({}, {'METADATA': 1})
        histogram = {'TAGS': {}}
        for log in logs:
            if 'TAGS' in log.METADATA:
                for row in csv.reader([log.METADATA['TAGS']]):
                    for tag in row:
                        if tag not in histogram['TAGS']:
                            histogram['TAGS'][tag] = {'NAME': tag, 'COUNT': 1}
                        else:
                            histogram['TAGS'][tag]['COUNT'] = histogram[
                                'TAGS'][tag]['COUNT'] + 1

        resp.respond(histogram)

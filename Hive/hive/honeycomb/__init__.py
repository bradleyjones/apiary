#!/usr/bin/env python
from hive.common.base import Base
import hive.common.lucenedriver
from routes import Routes
import sys
import lucene

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Honeycomb(Base):

    def __init__(self):
        Base.__init__(self, "honeycomb")


def main():
    honeycomb = Honeycomb()
    hive.common.lucenedriver.setup(honeycomb.config)
    honeycomb.start(Routes)

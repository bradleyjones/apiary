#!/usr/bin/env python
from hive.common.base import Base
import hive.common.lucenedriver
from routes import Routes
import sys
import lucene

class Honeycomb(Base):

    def __init__(self):
        Base.__init__(self, "honeycomb")

def main():
    honeycomb = Honeycomb()
    hive.common.lucenedriver.setup(honeycomb.config)
    honeycomb.start(Routes)

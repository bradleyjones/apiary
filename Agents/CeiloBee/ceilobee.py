#!/usr/bin/env python
from hive.common.base import Base
from routes import Routes


class CeiloBee(Base):

    def __init__(self):
        Base.__init__(self, "ceilobee")

def main():
    ceiloagent = CeiloBee()
    ceiloagent.start(Routes)

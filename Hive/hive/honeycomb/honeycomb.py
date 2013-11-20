#!/usr/bin/env python
from ..common.base import Base
from routes import Routes
import signal
import sys

class Honeycomb(Base):

    def __init__(self):
        Base.__init__(self, "honeycomb")


def exit(signal, frame):
    sys.exit(0)

def main():
    honeycomb = Honeycomb()
    honeycomb.start(Routes)

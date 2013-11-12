#!/usr/bin/env python
from ..common.base import Base
from routes import Routes


class Honeycomb(Base):

    def __init__(self):
        Base.__init__(self, "honeycomb")


def main():
    honeycomb = Honeycomb()
    honeycomb.start(Routes)

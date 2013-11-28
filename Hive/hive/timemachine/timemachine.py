#!/usr/bin/env python
from ..common.base import Base
from routes import Routes


class TimeMachine(Base):

    def __init__(self):
        Base.__init__(self, "timemachine")


def main():
    timemachine = TimeMachine()
    timemachine.start(Routes)

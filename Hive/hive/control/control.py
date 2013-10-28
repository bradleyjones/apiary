#!/usr/bin/env python
from ..common.base import Base
import controller
import routes
from markagentthread import MarkAgentsThread

class Control(Base):

    def __init__(self):
        Base.__init__(self, "control")
        self.agentsThread = MarkAgentsThread(self.config)

    def extraThreads(self):
        self.agentsThread.start()


def main():
    control = Control()
    control.start(routes, controller)

#!/usr/bin/env python
from ..common.base import Base
import controller
import routes


class Control(Base):

    def __init__(self):
        Base.__init__(self, "control")

    def migrate(self):


def main():
    control = Control()
    control.startServer(routes, controller)

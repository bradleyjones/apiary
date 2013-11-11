#!/usr/bin/env python
from ..common.base import Base
from routes import Routes


class Control(Base):

    def __init__(self):
        Base.__init__(self, "control")


def main():
    control = Control()
    control.start(Routes)

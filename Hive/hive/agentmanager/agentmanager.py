#!/usr/bin/env python
from ..common.base import Base
from routes import Routes


class AgentManager(Base):

    def __init__(self):
        Base.__init__(self, "agentmanager")


def main():
    agentmanager = AgentManager()
    agentmanager.start(Routes)

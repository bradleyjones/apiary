#!/usr/bin/env python
"""Manager for Agents in the Apiary ecosystem, provides registration and
configuration management."""

from ..common.base import Base
from routes import Routes

__author__ = "Sam Betts"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Brad Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class AgentManager(Base):

    def __init__(self):
        Base.__init__(self, "agentmanager")


def main():
    agentmanager = AgentManager()
    agentmanager.start(Routes)

import uuid
import random
import json
from ..common.controller import Controller as Parent
from agent import Agent
import time


class Controller(Parent):

    def models(self):
        self.agents = Agent(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def heartbeat(self, data, resp):
        self.logger.debug("Received HeartBeat from: %s", data["from"])
        agent = self.agents.find(data["from"])
        agent.HEARTBEAT = time.time()
        agent.DEAD = False
        self.agents.save(agent)

    def data(self, data, resp):
        pass

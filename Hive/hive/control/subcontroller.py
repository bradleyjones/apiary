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

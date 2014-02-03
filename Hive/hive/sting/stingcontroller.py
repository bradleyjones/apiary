import uuid
import random
import json
from ..common.controller import Controller as Parent
import time


class Controller(Parent):

    def models(self):
        self.users = User(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS



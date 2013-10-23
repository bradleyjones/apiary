import uuid
import random
import json
from ..common.controller import Controller as Parent


class Controller(Parent):

    def extra_data(self):
        self.agents = {}

    def handshake(self, data, resp):
        # Make sure uuid always starts with a letter because not valid
        # to have xml tag start with a number
        id = str(uuid.uuid4())
        self.agents[id] = data
        self.event(json.dumps(self.agents[id]), 'agents')
        resp.respond(id)

    def goodbye(self, data, resp):
        del self.agents[data]
        resp.respond("GOODBYE!")

    def get_agents(self, data, resp):
        response = {}
        response['agents'] = self.agents
        resp.respond(json.dumps(response))

    def get_single_agent(self, data, resp):
        resp.respond(json.dumps(self.agent[data]))

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

import uuid
import random
import json
from ..common.controller import Controller as Parent
from agent import Agent
import time 
from threading import Timer

class Controller(Parent):

    def extra_data(self):
        self.agents = {}

    def remove_dead_agents(self):
        for id, agent in self.agents.iteritems():
            if agent.last_heard + 900 >= time.time():
                agent.set_dead()
                self.send_agent_event(agent)

    def send_agent_event(self, agent):
        event = {}
        event[agent.id] = {}
        event[agent.id]['dead'] = agent.dead
        event[agent.id]['lastheard'] = agent.last_heard
        self.event(json.dumps(event), 'agents')

    def handshake(self, data, resp):
        # Make sure uuid always starts with a letter because not valid
        # to have xml tag start with a number
        id = str(uuid.uuid4())
        agent = Agent(id, time.time())
        self.agents[id] = agent
        self.send_agent_event(agent)
        resp.respond(id)

    def goodbye(self, data, resp):
        del self.agents[data]
        resp.respond("GOODBYE!")

    def get_agents(self, data, resp):
        response = {}
        response['agents'] = {}
        for agent in self.agents:
            response['agents'][agent.id] = {}
            response['agents'][agent.id]['dead'] = agent.dead
            response['agents'][agent.id]['lastheard'] = agent.last_heard
        resp.respond(json.dumps(response))

    def get_single_agent(self, data, resp):
        resp.respond(json.dumps(self.agent[data]))

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

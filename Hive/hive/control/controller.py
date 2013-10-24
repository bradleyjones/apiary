import uuid
import random
import json
from ..common.controller import Controller as Parent
from agent import Agent, AgentModel
import time 
from threading import Timer

class Controller(Parent):

    def extra_data(self):
        self.agents = AgentModel(self.config)

    def remove_dead_agents(self):
        pass

    def send_agent_event(self, agent):
        event = self.make_agent_message(agent, {})
        self.event(json.dumps(event), 'agents')

    def make_agent_message(self, agent, response):
        response[agent.id] = {}
        response[agent.id]['dead'] = bool(agent.dead)
        response[agent.id]['heartbeat'] = agent.heartbeat
        return response

    def handshake(self, data, resp):
        # Make sure uuid always starts with a letter because not valid
        # to have xml tag start with a number
        id = str(uuid.uuid4())
        agent = Agent(id, time.time())
        self.agents.save(agent)
        self.send_agent_event(agent)
        resp.respond(id)

    def goodbye(self, data, resp):
        agent = self.agents.find(data)
        self.agents.delete(agent)
        resp.respond("GOODBYE!")

    def get_agents(self, data, resp):
        agents = self.agents.findAll()
        response = {}
        for key, agent in agents.iteritems():
            response = self.make_agent_message(agent, response)
        resp.respond(json.dumps(response))

    def get_single_agent(self, data, resp):
        agent = self.agents.find(data)
        response = self.make_agent_message(agent, {})
        resp.respond(json.dumps(response))

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

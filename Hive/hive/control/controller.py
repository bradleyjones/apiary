import uuid
import random
import json
from ..common.controller import Controller as Parent
from agent import Agent, AgentModel
import time


class Controller(Parent):

    def extra_data(self):
        self.agents = AgentModel(self.config)

    def send_agent_event(self, agent):
        event = {}
        event[agent.id] = agent.to_hash()
        self.event(json.dumps(event), 'agents')

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def handshake(self, data, resp):
        id = str(uuid.uuid4())
        agent = Agent(id, time.time())
        self.agents.save(agent)
        self.send_agent_event(agent)
        resp.respond(id)

    def heartbeat(self, data, resp):
        agent = self.agents.find(data["from"])
        agent.heartbeat = time.time()
        self.agents.save(agent)

    def goodbye(self, data, resp):
        agent = self.agents.find(data["from"])
        self.agents.delete(agent)
        resp.respond("GOODBYE!")

    def get_agents(self, data, resp):
        agents = self.agents.findAll()
        response = {}
        for key, agent in agents.iteritems():
            response[agent.id] = agent.to_hash()
        resp.respond(json.dumps(response))

    def get_single_agent(self, data, resp):
        agent = self.agents.find(data["data"])
        response = {}
        response[agent.id] = agent.to_hash()
        resp.respond(json.dumps(response))

    def authenticate(self, data, resp):
        agent = self.agents.find(data["data"])
        agent.authenticated = True
        self.logger.info("Authenticating Agent: %s", agent.id) 
        self.agents.save(agent)
        self.send_agent_event(agent)

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

import uuid
import random
import json
from ..common.controller import Controller as Parent
from agent import Agent
import time


class RPCController(Parent):

    def models(self):
        self.agents = Agent(self.config)

    def send_agent_event(self, agent):
        event = {}
        event[agent.UUID] = agent.to_hash()
        self.event(json.dumps(event), 'agents')

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def handshake(self, data, resp):
        id = str(uuid.uuid4())
        agent = self.agents.new()
        agent.UUID = id
        agent.HEARTBEAT = time.time()
        agent.DEAD = False
        agent.AUTHENTICATED = False
        agent.QUEUE = data['reply_to']
        self.agents.save(agent)
        self.send_agent_event(agent)
        resp.respond(id)

    def heartbeat(self, data, resp):
        self.logger.debug("Received HeartBeat from: %s", data["from"])
        agent = self.agents.find(data["from"])
        agent.HEARTBEAT = time.time()
        agent.DEAD = False
        self.agents.save(agent)

    def goodbye(self, data, resp):
        agent = self.agents.find(data["from"])
        self.agents.delete(agent)
        resp.respond("GOODBYE!")

    def get_agents(self, data, resp):
        agents = self.agents.findAll()
        response = {}
        for key, agent in agents.iteritems():
            response[agent.UUID] = agent.to_hash()
        resp.respond(response)

    def get_single_agent(self, data, resp):
        agent = self.agents.find(data["data"])
        response = None
        if agent is not None:
            response = {}
            response[agent.UUID] = agent.to_hash()
        resp.respond(response)

    def authenticate(self, data, resp):
        agent = self.agents.find(data["data"])
        agent.AUTHENTICATED = True
        self.logger.info("Authenticating Agent: %s", agent.UUID)
        self.agents.save(agent)
        self.send_agent_event(agent)

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

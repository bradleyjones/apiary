"""Controller for actions relating to agents thats not configuration."""

import uuid
import random
import json
from ..common.controller import Controller as Parent
from agent import Agent
import time

__author__ = "Sam Betts, Bradley Jones"
__credits__ = ["Sam Betts", "John Davidge", "Jack Fletcher", "Bradley Jones"]
__license__ = "Apache v2.0"
__version__ = "1.0"


class Controller(Parent):

    def models(self):
        self.agents = Agent(self.config)

    def send_agent_event(self, agent, key):
        event = {"agents": {}}
        event['agents'][agent.UUID] = agent.to_hash()
        self.event(event, 'agent.%s' % key)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def handshake(self, data, resp):
        id = str(uuid.uuid4())
        agent = self.agents.new()
        agent.UUID = id
        agent.HEARTBEAT = time.time()
        agent.DEAD = False
        agent.AUTHENTICATED = False
        agent.QUEUE = data['reply_to']
        agent.MACHINEID = data['machineid']
        agent.BOUND = False
        agent.METADATA = {}
        agent = self.agents.save(agent)
        self.send_agent_event(agent, "new")
        resp.respond(id)

    def update(self, body, resp):
        agent = self.agents.find(body['data']['UUID'])
        for column in self.agents.columns:
            if column in body['data']:
                setattr(agent, column, body['data'][column])
        self.agents.save(agent)
        self.send_agent_event(agent, "update")
        resp.respond(agent.to_hash())

    def goodbye(self, data, resp):
        agent = self.agents.find(data["from"])
        self.agents.delete(agent)
        resp.respond("GOODBYE!")

    def get_agents(self, data, resp):
        agents = self.agents.findAll()
        response = {}
        for agent in agents:
            response[agent.UUID] = agent.to_hash()
        resp.respond(response)

    def get_agents_count(self, data, resp):
        agents = self.agents.findAll()
        count = len(agents)
        resp.respond(count)

    def get_single_agent(self, data, resp):
        agent = self.agents.find(data["data"]["id"])
        response = None
        if agent is not None:
            response = {}
            response[agent.UUID] = agent.to_hash()
        resp.respond(response)

    def heartbeat(self, data, resp):
        self.logger.debug("Received HeartBeat from: %s", data["from"])
        agent = self.agents.find(data["from"])
        agent.HEARTBEAT = time.time()
        agent.DEAD = False
        self.agents.save(agent)

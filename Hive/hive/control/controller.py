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
        t = Timer(30, self.mark_dead_agents, ())
        t.daemon = True
        t.start()

    def mark_dead_agents(self):
        self.logger.info("Scanning for Dead Agents...")
        agentmodel = AgentModel(self.config)
        agents = agentmodel.findAll()
        for key, agent in agents.iteritems():
            if (agent.heartbeat + 300) < time.time():
                agent.dead = True
                self.logger.info("Agent %s is Dead!", agent.id)
                self.send_agent_event(agent)
                agentmodel.save(agent)
        t = Timer(30, self.mark_dead_agents, ())
        t.daemon = True
        t.start()

    def send_agent_event(self, agent):
        event = self.make_agent_message(agent, {})
        self.event(json.dumps(event), 'agents')

    def make_agent_message(self, agent, response):
        response[agent.id] = {}
        response[agent.id]['dead'] = bool(agent.dead)
        response[agent.id]['heartbeat'] = agent.heartbeat
        return response

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
            response = self.make_agent_message(agent, response)
        resp.respond(json.dumps(response))

    def get_single_agent(self, data, resp):
        agent = self.agents.find(data["data"])
        response = self.make_agent_message(agent, {})
        resp.respond(json.dumps(response))

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

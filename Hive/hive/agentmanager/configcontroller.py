import json
from ..common.controller import Controller as Parent
from ..common.rpcsender import RPCSender
from agent import Agent


class Controller(Parent):

    def models(self):
        self.agents = Agent(self.config)
        self.sender = RPCSender(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def setFiles(self, body, resp):
        response = []
        for agent in body['data']['agents']: 
            ag = self.agents.find(agent)
            r = sender.send_message('SETFILES', agent, body['data']['files'], key=ag.QUEUE) 
            response.append(r)
        resp.respond(response)

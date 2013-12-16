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
        data = json.loads(body['data'])
        for agent in data['agents']:
            ag = self.agents.find(agent)
            r = self.sender.send_request(
                'SETFILES',
                agent,
                data['files'],
                '000000000000',
                'agentmanager',
                key=ag.QUEUE)
            response.append(r)
        resp.respond(response)

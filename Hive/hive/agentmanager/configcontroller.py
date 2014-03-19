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
        data = body['data']
        # Create body for sending to agent
        sbody = {"files": data['files']}
        for agent in data['agents']:
            ag = self.agents.find(agent)
            if ag is not None:
                self.logger.info("Sending %s to %s" % (sbody, agent))
                r = { agent : self.sender.send_request(
                    'SETFILES',
                    agent,
                    sbody,
                    '000000000000',
                    'agentmanager',
                    key=ag.QUEUE) }
                self.logger.info("Sent!")
            else:
                r = { agent : 'Agent Doesnt Exist!' }
            response.append(r)
        resp.respond(response)

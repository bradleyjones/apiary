import uuid
import xml.etree.cElementTree as ET


class Controller(object):

    def __init__(self):
        self.agents = {}

    def handshake(self, data, resp):
        id = str(uuid.uuid4())
        self.agents[id] = data
        resp.respond(id)

    def goodbye(self, data, resp):
        del self.agents[data]
        resp.respond("GOODBYE!")

    def get_agents(self, data, resp):
        response = ET.Element('agents')

        for uuid, agent in self.agents.iteritems():
            machineid = ET.SubElement(response, 'agent')
            machineid.text = uuid

        resp.respond(ET.tostring(response, encoding='utf8', method='xml'))

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

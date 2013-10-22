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

        for uuid, machineid in self.agents.iteritems():
            agent = ET.SubElement(response, 'agent')
            uid = ET.SubElement(agent, 'id')
            uid.text = uuid
            machid = ET.SubElement(agent, 'machineid')
            machid.text = machineid

        resp.respond(ET.tostring(response, encoding='utf8', method='xml'))

    def get_single_agent(self, data, resp):
        agent = ET.Element('agent')

        if data in self.agents:
          uid = ET.SubElement(agent, 'id')
          uid.text = data
          machid = ET.SubElement(agent, 'machineid')
          machid.text = self.agents[data]

        resp.respond(ET.tostring(agent, encoding='utf8', method='xml'))

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")

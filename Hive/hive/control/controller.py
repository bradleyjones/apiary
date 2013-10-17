import uuid
import xml.etree.cElementTree as ET


class Controller(object):

    def __init__(self):
        self.agents = {}

    def handshake(self, data):
        id = str(uuid.uuid4())
        self.agents[id] = data
        return id

    def goodbye(self, data):
        del self.agents[data]
        return "GOODBYE!"

    def get_agents(self, data):
        response = ET.Element('agents')

        for uuid, agent in self.agents.iteritems():
            machineid = ET.SubElement(response, 'agent')
            machineid.text = uuid

        return ET.tostring(response, encoding='utf8', method='xml')

    def default(self, data):
        return "THIS IS THE DEFAULT ACTION"

import uuid
import random
import xml.etree.cElementTree as ET
from ..common.pubsubserver import PubSubServer

class Controller(object):

    def __init__(self):
        self.agents = {}
        self.pubsub = PubSubServer('events','127.0.0.1','agents')

    #Build XML for single agent
    def xml_agent(self, data):
        agent = ET.Element('agent')

        if data in self.agents:
          uid = ET.SubElement(agent, 'id')
          uid.text = data
          machid = ET.SubElement(agent, 'machineid')
          machid.text = self.agents[data]

        return ET.tostring(agent, encoding='utf8', method='xml')

    def handshake(self, data, resp):
        # Make sure uuid always starts with a letter because not valid
        # to have xml tag start with a number
        id = chr(random.randrange(97, 97 + 26 + 1)) + str(uuid.uuid4())
        self.agents[id] = data
        self.pubsub.publish_msg(self.xml_agent(id), 'agents')
        resp.respond(id)

    def goodbye(self, data, resp):
        del self.agents[data]
        resp.respond("GOODBYE!")

    def get_agents(self, data, resp):
        response = ET.Element('agents')

        for uuid, machineid in self.agents.iteritems():
            agent = ET.SubElement(response, uuid)
            machid = ET.SubElement(agent, 'machineid')
            machid.text = machineid

        resp.respond(ET.tostring(response, encoding='utf8', method='xml'))

    def get_single_agent(self, data, resp):
        resp.respond(self.xml_agent(data))

    def default(self, data, resp):
        resp.respond("THIS IS THE DEFAULT ACTION")



import uuid
import pika
import json
import unittest
from hive.tests.basictest import HiveBasicTest
from hive.agentmanager.agentscontroller import Controller
from hive.common.rpcresponse import RPCResponse

class ControllerTests(HiveBasicTest):

    UUID = None

    def setUp(self):
        self.controller = Controller(self.config)

    def handshake(self):
        data = {}
        data['action'] = "HANDSHAKE"
        data['to'] = "agentmanager"
        data['from'] = "Unknown"
        data['data'] = ""
        data['machineid'] = "testmachine"
        data['reply_to'] = "ASBDLHABSDJLHBASD"
        
        resp = RPCResponse()

        self.controller.handshake(data, resp)
        ControllerTests.uuid = resp.data

    def getsingle(self):
        data = {}
        data['action'] = "SINGLEAGENT"
        data['to'] = "agentmanager"
        data['from'] = ControllerTests.uuid
        data['data'] = ControllerTests.uuid
        data['machineid'] = "testmachine"

        resp = RPCResponse()
        self.controller.get_single_agent(data, resp)
        result = resp.data

        self.assertTrue(result[ControllerTests.uuid]['UUID'] == ControllerTests.uuid)

    def heartbeat(self):
        data = {}
        data['action'] = "HEARTBEAT"
        data['to'] = "agentmanager"
        data['from'] = ControllerTests.uuid
        data['data'] = ""
        data['machineid'] = "testmachine"

        resp = RPCResponse()
        self.controller.heartbeat(data, resp)

    def goodbye(self):
        data = {}
        data['action'] = "GOODBYE"
        data['to'] = "agentmanager"
        data['from'] = ControllerTests.uuid
        data['data'] = ""
        data['machineid'] = "testmachine"

        resp = RPCResponse()
        self.controller.goodbye(data, resp)
        self.assertTrue(resp.data == 'GOODBYE!')
    
    def getagents(self):
        data = {}
        data['action'] = "ALLAGENTS"
        data['to'] = "agentmanager"
        data['from'] = ControllerTests.uuid
        data['data'] = ControllerTests.uuid
        data['machineid'] = "testmachine"

        resp = RPCResponse()
        self.controller.get_agents(data, resp)
        result = resp.data

        self.assertTrue(not (ControllerTests.uuid in result))


testSuite = unittest.TestSuite()
testSuite.addTest(ControllerTests('handshake', configname='agentmanager'))
testSuite.addTest(ControllerTests('getsingle', configname='agentmanager'))
testSuite.addTest(ControllerTests('heartbeat', configname='agentmanager'))
testSuite.addTest(ControllerTests('goodbye', configname='agentmanager'))
testSuite.addTest(ControllerTests('getagents', configname='agentmanager'))

unittest.TextTestRunner(verbosity=2).run(testSuite)

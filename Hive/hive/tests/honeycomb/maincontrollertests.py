from hive.tests.basictest import HiveBasicTest
from hive.honeycomb.databasecontroller import Controller
from hive.common.rpcresponse import RPCResponse
import unittest

class MainControllerTests(HiveBasicTest):
    
    def setUp(self):
        self.controller = Controller(self.config)

    def testSubscribe(self):
        resp = RPCResponse()
        data = { "action":"INSERT", "data":{ "Time":1234567, "Text":"DatabaseControllerTest" } }
        self.assertTrue(resp.data == 'OK')
    
    def testUnsubscribe(self):
        resp = RPCResponse()
        data = { "action":"INSERT", "data":{ "Time":1234567, "Text":"DatabaseControllerTest" } }
        self.assertTrue(resp.data[0]['Time'] == 1234567)

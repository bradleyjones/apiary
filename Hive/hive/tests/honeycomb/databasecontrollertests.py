from hive.tests.basictest import HiveBasicTest
from hive.honeycomb.databasecontroller import Controller
from hive.common.rpcresponse import RPCResponse
import unittest

class DatabaseControllerTests(HiveBasicTest):
    
    def setUp(self):
        self.controller = Controller(self.config)

    def testInsert(self):
        resp = RPCResponse()
        data = { "action":"INSERT", "data":{ "Time":1234567, "Text":"DatabaseControllerTest" } }
        self.assertTrue(resp.data == 'OK')
    
    def testFind(self):
        resp = RPCResponse()
        data = { "action":"INSERT", "data":{ "Time":1234567, "Text":"DatabaseControllerTest" } }
        self.assertTrue(resp.data[0]['Time'] == 1234567)

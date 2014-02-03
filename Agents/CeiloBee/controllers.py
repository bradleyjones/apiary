import uuid
import random
import json
import threading
import time
import keystoneclient.v2_0.client as ksclient
import ceilometerclient as ceiloclient
from hive.common.controller import Controller as Parent
from hive.common.simplepublisher import SimplePublisher
from openstack import Openstack
from uuid import getnode as get_mac


class Controller(Parent):

    def models(self):
        self.openstacks = Openstack(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def handshake(self, data, resp):

        class HeartBeater(threading.Thread):
            def __init__(self, clientID, heartbeatInterval):
                self.clientID = clientID
                self.heartbeatInterval = heartbeatInterval

            def run(self):
                while(1):
                   time.sleep(self.heartbeatInterval)
                   self.logger.debug("Sending HeartBeat")
                   message = {
                       "action": "HEARTBEAT"
                       "to": "AgentManager"
                       "from": self.clientID
                       "data": "Beat"
                       "machineID": get_mac()
                   }
                   self.publisher.publish(message,"agents"+self.clientID+".heartbeat")

        self.clientID = data.UUID
        self.heartbeater = HeartBeater(self.clientID, self.config['Agent']['heartbeatInterval'])
        self.heartbeater.start()
        self.logger.debug("Agent Initialised")

    def createOpenStack(self, data, resp):

        openstack = self.openstacks.new()

        keystone = ksclient.Client(auth_url="http://"+data.keystoneIPPort+"/v2.0",
            username=data.login,
            password=data.password,
            tenant_name=data.tenantName)

        ceilometer_endpoint = keystone.service_catalog.url_for(service_type='metering',
                                                               endpoint_type='adminURL')

        ceilometer = ceiloclient.Client('1', endpoint=ceilometer_endpoint, token=keystone.token-get())

        openstack.UUID = str(uuid.uuid4())
        openstack.IP = keystoneIPPort
        openstack.LOGIN = login
        openstack.PASSWORD = password
        openstack.TENANT = tenantName
        openstack.AUTHTOKEN = keystone.token-get()
        openstack.CEILOENDPOINT = ceilometer_endpoint
        openstack = self.openstacks.save(openstack)

        resp.respond(openstack.to_hash())

    def removeOpenStack(self, data, resp):
        print data.keystoneIP

    def getOpenStacks(self, data, resp):
        openstackList = self.openstacks.findAll()
        resp.respond(openstackList)

    def getmeters(self, data, resp):
        openstack = self.openstacks.find(body['data']['UUID'])
        ceilometer = ceiloclient.Client(endpoint=openstack['data']['CEILOENDPOINT'], token=openstack['data']['AUTHTOKEN'])
        meters = ceilometer.meters.list()
        resp.respond(meters)

    def setMeterListener(self, data, resp):
        openstack = self.openstacks.find(body['data']['UUID'])
        ceilometer = ceilocleint.Cleint(endpoint=openstack['data']['CEILOENDPOINT'], token=openstack['data']['AUTHTOKEN'])
        meter = data.meterName
        sampleRate = data.sampleRate

        class MeterListener(threading.Thread):
            def __init__(self, ceilometer, meter, sampleRate):
                self.ceilometer = ceilometer
                self.meter = meter
                self.sampleRate = sampleRate

            def run(self):
                while(1):
                    time.sleep(self.sampleRate)
                    self.logger.debug("Sending Meter Samples")

                    payload = {
                        'CONTENT': ceilometer.meters.getMeter(meter)
                        'TYPE':"meter"
                        'EVENTTIMESTAMP':
                        'METADATA':{
                        }
                    }

                    message = {
                       "action":"DATA"
                       "to": "HoneyComb"
                       "from": self.clientID
                       "data": payload
                       "machineID": get_mac()
                    }
                    self.publisher.publish(message,"agents."+self.clientID+".data")

        meterListener = MeterListener(ceilometer, meter, sampleRate)
        meterListener.start()

    def removeListener(self, listenerID):

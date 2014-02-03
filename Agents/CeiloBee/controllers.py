import uuid
import random
import json
import threading
import time
import keystoneclient.v2_0.client as ksclient
import ceilometerclient import ceiloclient
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

    def createOpenStack(self, keystoneIPPort, login, password, tenantName):

        openstack = self.openstacks.new()

        keystone = ksclient.Client(auth_url="http://"+keystoneIPPort+"/v2.0",
            username=login,
            password=password,
            tenant_name=tenantName)

        ceilometer_endpoint = keystone.service_catalog.url_for(service_type='metering',
                                                               endpoint_type='adminURL')

        ceilometer = ceiloclient.Client('1', endpoint=ceilometer_endpoint, token=keystone.token-get())

        openstack.IP = keystoneIPPort
        openstack.LOGIN = login
        openstack.PASSWORD = password
        openstack.TENANT = tenantName
        openstack.AUTHTOKEN = keystone.token-get()
        openstack.CEILOENDPOINT = ceilometer_endpoint
        openstack = self.openstacks.save(openstack)

    def removeOpenStack(self, keystoneIP):

    def getOpenStacks(self):


    def getmeters(self, openstack):

    def setMeterListener(self, meterUUID, openstack, sampleRate):

    def removeListener(self, listenerID):

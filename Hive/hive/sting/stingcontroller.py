from ..common.controller import Controller as Parent
from pkg_resources import resource_filename
from apns import APNs, Payload
import pika
import json
import sys
from hive.sting.user import user
from hive.sting.device import device


class Controller(Parent):

    def models(self):
        self.users = user(self.config)
        self.devices = device(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def event(self, message, response):

        for user in self.users.find(message['USER']):
            for device in user.devices:
                device = self.devices.find(device)
                apns = APNs(use_sandbox=True, cert_file=(
                resource_filename(__name__,'apns/certs/ApiaryCert.pem')),
                key_file=(resource_filename(__name__,'apns/certs/ApiaryKey.pem')))
                token_hex = device.device_id
                payload = Payload(alert=message['TEXT'], sound="default", badge=0)
                apns.gateway_server.send_notification(token_hex, payload)
                print "Notification sent to device " + device.device_id 



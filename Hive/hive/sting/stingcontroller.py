from ..common.controller import Controller as Parent
from pkg_resources import resource_filename
from apns import APNS, Payload
import pika
import json
import sys

class Controller(Parent):

    def models(self):
        self.users = User(self.config)

    # BELOW THIS LINE ARE ALL CONTROLLER ACTIONS

    def callback(ch, method, properties, body):
        # Initialise Apple Push Notification System object
        apns = APNS(use_sandbox=True, cert_file=(
            resource_filename(__name__,'apns/certs/ApiaryCert.pem')),
            key_file=(resource_filename(__name__,'apns/certs/ApiaryKey.pem')))

        # Initialise String for message to be sent in alert
        alert_text = "None"
        
        # Load data from json recieved on message queue
        data = json.loads(body)

        # This implementation only looks at new/dead agents
        # Once user-definable alerts are implemented this will be extended
        for agent in data.values():
            uuid = agent["UUID"]
            if agent["DEAD"]:
                alert_text = "Agent " + uuid + " is Dead!"
            else:
                alert_text = "New Agent: " + uuid

        # Send the notification
        # Once userdefinable alerts are implemented the user's device will
        # be identified based on the user associated with the alert
        # For now we're using a single device
        token_hex = 'c337dce1b94e8908e3b9768516fed42c90b1dff0ad01dfe7334970227da0a229'
        payload = Payload(alert=alert_text, sound="default", badge=1)
        apns.gateway_server.send_notification(token_hex, payload)

        print "Notification Sent: " +alert_text

    def new_channel(connection, routing_key_name):

        # Initialise channel
        channel = connection.channel()

        # Configure channel
        channel.exchange_declare(exchange='apiary', type='topic')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(
            exchange='apiary',
            queue=queue_name,
            routing_key=routing_key_name)

        channel.basic_consume(callback, queue=queue_name, no_ack=False)

        return channel

    def main():

        # Define connection to rabbit
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='127.0.0.1'))

        # Define channels to listen on
        new_agent_channel = new_channel(
            connection,
            'events.agentmanager.agent.new')
        dead_agent_channel = new_channel(
            connection,
            'events.agentmanager.agent.dead')

        # Debug APNS Notification
        apns = APNS(use_sandbox=True, cert_file=(
            resource_filename(__name__,'apns/certs/ApiaryCert.pem')),
            key_file=(resource_filename(__name__,'apns/certs/ApiaryKey.pem')))
        token_hex = 'c337dce1b94e8908e3b9768516fed42c90b1dff0ad01dfe7334970227da0a229'
        payload = Payload(alert="Sting Running", sound="default", badge=0)
        apns.gateway_server.send_notification(token_hex, payload)
        #########################

        # Start channel consumers
        new_agent_channel.start_consuming()
        dead_agent_channel.start_consuming()

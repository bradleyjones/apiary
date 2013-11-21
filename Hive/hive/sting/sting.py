import pika
import json
from apns import APNs, Payload
from pkg_resources import resource_filename

import sys


def callback(ch, method, properties, body):
    apns = APNs(
        use_sandbox=True, cert_file=(
            resource_filename(__name__, 'apns/certs/ApiaryCert.pem')),
        key_file=(resource_filename(__name__, 'apns/certs/ApiaryKey.pem')))

    alert_text = "NONE"
    data = json.loads(body)
    for agent in data.values():
      if agent["DEAD"]:
        alert_text = "Agent " + agent["UUID"] + " is Dead!"
      else:
        alert_text = "New Agent: " + agent["UUID"]

    # Send a notification
    # Need to implement database of registered users and their devices
    token_hex = 'c337dce1b94e8908e3b9768516fed42c90b1dff0ad01dfe7334970227da0a229'
    # Need to implement analysis of event so relevant message can be pushed
    payload = Payload(alert=alert_text, sound="default", badge=1)
    # For each message for each user
    apns.gateway_server.send_notification(token_hex, payload)

    print alert_text

def main():

    # Define connection to rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))

    # Define channels to listen on
    new_agent_channel = connection.channel()
    dead_agent_channel = connection.channel()

    # Configure new_agent_channel
    new_agent_channel.exchange_declare(exchange='apiary', type='topic')

    result = new_agent_channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    new_agent_channel.queue_bind(exchange='apiary', queue=queue_name, routing_key='events.agentmanager.agent.new')

    new_agent_channel.basic_consume(callback, queue=queue_name, no_ack=False)

    # Configure dead_agent_channel
    dead_agent_channel.exchange_declare(exchange='apiary', type='topic')

    result = dead_agent_channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    dead_agent_channel.queue_bind(exchange='apiary', queue=queue_name, routing_key='events.agentmanager.agent.dead')

    dead_agent_channel.basic_consume(callback, queue=queue_name, no_ack=False)

    # Start channel consumers
    new_agent_channel.start_consuming()
    print "Listenting for new agents on events.agentmanager.agent.new"
    dead_agent_channel.start_consuming()
    print "Listenting for dead agents on events.agentmanager.agent.dead"

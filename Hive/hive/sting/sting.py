import pika
from apns import APNs, Payload
from pkg_resources import resource_filename

import sys


def callback(ch, method, properties, body):
    apns = APNs(
        use_sandbox=True, cert_file=(
            resource_filename(__name__, 'apns/certs/ApiaryCert.pem')),
        key_file=(resource_filename(__name__, 'apns/certs/ApiaryKey.pem')))

    # Send a notification
    token_hex = 'c337dce1b94e8908e3b9768516fed42c90b1dff0ad01dfe7334970227da0a229'
    payload = Payload(alert="New Agent Registered!", sound="default", badge=1)
    apns.gateway_server.send_notification(token_hex, payload)


def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='25.199.138.99'))
    channel = connection.channel()

    channel.exchange_declare(exchange='events',
                             type='topic')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='events',
                       queue=queue_name,
                       routing_key='control.agents')

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()

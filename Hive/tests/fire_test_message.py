import uuid
import pika
import json

resp = None
corr_id = str(uuid.uuid4())


def on_response(ch, method, props, body):
    global resp, corr_id
    if corr_id == props.correlation_id:
        resp = body

data = {}
data['action'] = "HANDSHAKE"
data['to'] = "control"
data['from'] = "Unknown Worker"
data['data'] = "d563187e-c876-4553-9ff8-6e1bc7b8b600"
data['machineid'] = "havsbdjhlbasd"

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.1.106'))

channel = connection.channel()

result = channel.queue_declare(exclusive=True)

callback_queue = result.method.queue

channel.basic_consume(on_response, no_ack=True,
                      queue=callback_queue)

channel.basic_publish(exchange='',
                      routing_key='control',
                      properties=pika.BasicProperties(
                          reply_to=callback_queue,
                          correlation_id=corr_id,
                      ),
                      body=json.dumps(data))

while resp is None:
    connection.process_data_events()

print resp

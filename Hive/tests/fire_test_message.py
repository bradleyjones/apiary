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
#data['action'] = "HANDSHAKE"
#data['action'] = "SINGLEAGENT"
#data['action'] = "ALLAGENTS"
data['action'] = "HEARTBEAT"
data['to'] = "control"
data['from'] = "Unknown Worker"
data['data'] = "3964731e-b7e4-45e6-8a50-266f899faea6"
data['machineid'] = "havsbdjhlbasd"

credentials = pika.PlainCredentials('apiary', 'bees')

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.1.106', credentials=credentials))

channel = connection.channel()

result = channel.queue_declare(exclusive=True)

callback_queue = result.method.queue

#channel.basic_consume(on_response, no_ack=True,
#                      queue=callback_queue)

channel.basic_publish(exchange='apiary',
                      routing_key='data.GHJAVSDV',
#                      properties=pika.BasicProperties(
#                          reply_to=callback_queue,
#                          correlation_id=corr_id,
#                      ),
                     body=json.dumps(data))

#while resp is None:
#    connection.process_data_events()

print resp

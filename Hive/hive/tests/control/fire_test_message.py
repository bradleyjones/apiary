import uuid
import pika
import json
from configobj import ConfigObj, ConfigObjError

resp = None
corr_id = str(uuid.uuid4())


def on_response(ch, method, props, body):
    global resp, corr_id
    if corr_id == props.correlation_id:
        resp = body


def loadConfig(filepath):
    try:
        return ConfigObj(filepath, file_error=True)
    except (ConfigObjError, IOError) as e:
        logging.error("Config File Doesn't Exist: %s", filepath)
        raise SystemExit

config = loadConfig('config.ini')

data = {}
#data['action'] = "HANDSHAKE"
#data['action'] = "SINGLEAGENT"
#data['action'] = "ALLAGENTS"
#data['action'] = "HEARTBEAT"
#data['action'] = "AUTHENTICATE"
data['action'] = "RELEASE"
data['to'] = "control"
data['from'] = "Unknown Worker"
data['data'] = "7beaecc1-d100-433b-803f-59920cc4dd20"
data['machineid'] = "havsbdjhlbasd"

credentials = pika.PlainCredentials(config['Rabbit']['username'], config['Rabbit']['password'])

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=config['Rabbit']['host'], credentials=credentials))

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

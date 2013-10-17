import uuid
import pika
import xml.etree.cElementTree as ET

resp = None
corr_id = str(uuid.uuid4())


def on_response(ch, method, props, body):
    global resp, corr_id
    if corr_id == props.correlation_id:
        resp = body

response = ET.Element('message')

action = ET.SubElement(response, 'action')
action.text = 'AGENTS'

to = ET.SubElement(response, 'to')
to.text = 'control'

fro = ET.SubElement(response, 'from')
fro.text = 'Test_Ap'

data = ET.SubElement(response, 'data')
data.text = ""

machineid = ET.SubElement(response, 'machineid')
machineid.text = "GOD"

xml = ET.tostring(response, encoding='utf8', method='xml')

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
                      body=xml)

while resp is None:
    connection.process_data_events()

print resp

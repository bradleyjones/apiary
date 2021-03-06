import pika

def on_message(channel, method_frame, header_frame, body):
  print body

credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(
pika.ConnectionParameters(host="192.168.1.106", credentials=credentials))
channel = connection.channel()

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='apiary',
                 queue=queue_name,
                 routing_key="events.pheromone.alert")

channel.basic_consume(on_message, queue=queue_name, no_ack=True)
channel.start_consuming()


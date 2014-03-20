import pika

def on_message(channel, method_frame, header_frame, body):
  print body

credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(
pika.ConnectionParameters(host="192.168.1.106", credentials=credentials))
channel = connection.channel()
channel.basic_consume(on_message, queue="amq.gen-QJ4jaMCapbrhQZPhpP6IOL", no_ack=True)
channel.start_consuming()


"""
A helper class for wrapping the creation and consuming of a queue
using rabbit.
"""

import pika

class RPCServer(object):

  def __init__(self, name, host, func):
    self.queue = name
    self.host = host
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
    self.channel = connection.channel()
    channel.queue_declare(queue=self.queue)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(func, queue=queue)
    channel.start_consuming()
    print "Server Started, Ready for Requests!"

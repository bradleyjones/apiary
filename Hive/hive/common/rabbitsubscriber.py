import threading


class RabbitSubscriber(threading.Thread):

    def __init__(self):
        super(RabbitSubscriber, self).__init__()
        self.daemon = True

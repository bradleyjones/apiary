import uuid

class Controller(object):
    
    def __init__(self):
        self.agents = {}
    
    def handshake(self, data):
        id = str(uuid.uuid4())
        self.agents[id] = data 
        return id

    def default(self, data):
        return "THIS IS THE DEFAULT ACTION"

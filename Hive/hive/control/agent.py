class Agent(object):

  def __init__(self, id, last_heard): 
    self.id = id
    self.dead = False
    self.last_heard = last_heard
  
  def set_dead(self): 
    self.dead = True

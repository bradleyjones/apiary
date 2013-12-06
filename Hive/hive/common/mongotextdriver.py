from pymongo import MongoClient

class Driver(object):

  def __init__(self, config): 
      self.client = MongoClient("mongodb://%s:%s" % (config['Database']['mongodb_host'],
                  config['Database']['mongodb_port']))
      self.columns = []
      self.tablename = self.__class__.__name__ + "s"
      self.name = config['Database']['name']
      self.table = self.client[self.name][self.tablename]

  def index(self, fields, record):
    for field in fields:
      self.table.ensureIndex( { field: "text" } )

  def updateindex(self, fields, record):
    for field in fields:
      self.table.ensureIndex( { field: "text" } )

  def removeindex(self, fields, record):
    pass

  def query(self, query, fields):
    q = self.table.runCommand("text", { search: query })

    return q['results']

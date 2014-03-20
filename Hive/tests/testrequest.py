from hive.common.rpcsender import RPCSender
import time
import json

data = {}
data['CONTENT'] = "ERROR 128.10.10.90"
data['TYPE'] = "string"
data['EVENTTIMESTAMP'] = str(time.time())
data['METADATA'] = {}
data['METADATA']['TAGS'] = "firewall,yomama" 
data['QUERY'] = "CONTENT:\"ERROR *.*.*.*\"" 
data['TIMESCALE'] = "86400" 
data['files'] = {'PATH': "/etc/path", 'TAGS': "firewall"}
data['agents'] = ['17af7719-f759-44a5-95a6-f66d31c53f86']

data['query'] = "CONTENT:apple"
data['time'] = 600
data['quantity'] = 5
data['message'] = "HOLY MOTHER OF JEBUS"
data['user'] = "532b69a3dada5ac85667ba66"

sdata = data
 
config = {}
config['Rabbit'] = {}
config['Rabbit']['username'] = 'guest'
config['Rabbit']['password'] = 'guest'
config['Rabbit']['host'] = '127.0.0.1'

sender = RPCSender(config)

#resp = sender.send_request('DATA', 'hive', sdata, 'LKJABSDHBAS', 'Test Script', exchange="", key="honeycomb")
resp = sender.send_request('NEW', 'hive', sdata, 'LKJABSDHBAS', 'Test Script', exchange="", key="pheromone")

print resp

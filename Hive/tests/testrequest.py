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

sdata = data
 
config = {}
config['Rabbit'] = {}
config['Rabbit']['username'] = 'guest'
config['Rabbit']['password'] = 'guest'
config['Rabbit']['host'] = '192.168.1.106'

sender = RPCSender(config)

resp = sender.send_request('QUERY', 'hive', sdata, 'LKJABSDHBAS', 'Test Script', exchange="", key="honeycomb")

print resp

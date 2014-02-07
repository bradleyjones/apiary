from hive.common.rpcsender import RPCSender
import time
import json

data = {}
data['CONTENT'] = "ERROR 128.10.10.3"
data['TYPE'] = "string"
data['EVENTTIMESTAMP'] = str(time.time())
data['METADATA'] = {}

sdata = data

#sdata = "CONTENT:\"ERROR *.*.*.*\""
 
config = {}
config['Rabbit'] = {}
config['Rabbit']['username'] = 'guest'
config['Rabbit']['password'] = 'guest'
config['Rabbit']['host'] = '192.168.1.106'

sender = RPCSender(config)

resp = sender.send_request('DATA', 'hive', sdata, 'LKJABSDHBAS', 'Test Script', key='honeycomb')

print resp

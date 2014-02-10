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
config['Rabbit']['host'] = '127.0.0.1'

sender = RPCSender(config)

resp = sender.send_request('DATA', 'hive', sdata, 'LKJABSDHBAS', 'Test Script', exchange="apiary", key='agents.4dd78cf7-ad26-4ecb-b916-3ff883aeac52.heartbeat')

print resp

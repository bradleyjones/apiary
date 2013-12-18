from hive.common.rpcsender import RPCSender
import time
import json

data = {}
data['CONTENT'] = "OMGWTFBBQ"
data['TYPE'] = "file"
data['EVENTTIMESTAMP'] = str(time.time())
data['METADATA'] = {}

sdata = json.dumps(data)

config = {}
config['Rabbit'] = {}
config['Rabbit']['username'] = 'guest'
config['Rabbit']['password'] = 'guest'
config['Rabbit']['host'] = '127.0.0.1'

sender = RPCSender(config)

resp = sender.send_request('FINDALL', 'hive', sdata, 'LKJABSDHBAS', 'Test Script', key='honeycomb')

print resp

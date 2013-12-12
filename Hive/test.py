from hive.common.rpcsender import RPCSender
import time

data = {}
data['CONTENT'] = "OMGWTFBBQ"
data['TYPE'] = "file"
data['TIMESTAMP'] = str(time.time())
data['METADATA'] = {}

config = {}
config['Rabbit'] = {}
config['Rabbit']['username'] = 'guest'
config['Rabbit']['password'] = 'guest'
config['Rabbit']['host'] = '192.168.1.106'

sender = RPCSender(config)

resp = sender.send_request('DATA', 'honeycomb', data, 'LKJABSDHBAS', 'Test Script', key='honeycomb')

print resp

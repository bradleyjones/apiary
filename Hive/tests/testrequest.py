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

sdata = data
 
config = {}
config['Rabbit'] = {}
config['Rabbit']['username'] = 'guest'
config['Rabbit']['password'] = 'guest'
config['Rabbit']['host'] = '192.168.1.106'

sender = RPCSender(config)

resp = sender.send_request('SETFILES', 'hive', sdata, 'LKJABSDHBAS', 'Test Script', exchange="", key="agentmanager")

print resp

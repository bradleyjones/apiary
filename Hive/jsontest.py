import json 

sbody = json.dumps({ "files": ['asd', 'ads'] })

lsdf = json.dumps(sbody)

j = json.dumps('boods')

print j
print lsdf
print sbody

print type(j)
print type(lsdf)
print type(sbody)

print type(json.loads(j))
print type(json.loads(lsdf))
print type(json.loads(sbody))

print json.loads(j)
print json.loads(lsdf)
print json.loads(sbody)

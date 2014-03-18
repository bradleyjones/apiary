#!/bin/bash
# Drop mongo databases used by apiary
#

mongo agentmanager --eval "db.dropDatabase()"
mongo honeycomb --eval "db.dropDatabase()"
mongo queen-users --eval "db.dropDatabase()"
mongo queensessions --eval "db.dropDatabase()"

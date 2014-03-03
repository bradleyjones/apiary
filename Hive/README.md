The Hive
========

The middleware for the Apiary stack.

Components
----------

Common - The common components used by all the Hive services

AgentManager, AgentMonitor - These components manage the connection and configuration of agents. 

Honeycomb - Controls insertion and collection of data from the database software via an API.

TimeMachine - A service for retreiving streams of live and historic data.

Pheromone - An alert system that uses honeycomb lucene querys and user parameters.

Sting - A apiary hook into the Apple push notification service.

Installing Hive
---------------

* Copy installrc.example to installrc
* Edit installrc to match your environment
* Run ./install.sh *BEWARE* If running this a second time it will overwrite any modifications made to the apiary configs.


Running Hive on localhost
-------------------------

* Run "cp localrc.example localrc" to configure the start script
* Run "./start.sh" to begin all the services in a screen session.
* To access the screen session run "screen -x hive"
* Run "./stop.sh" to end the screen session created by start.sh

Current Binarys
---------------

* apiary-honeycomb    -> Starts Honeycomb server
* apiary-agentmanager -> Starts Agent Manager
* apiary-agentmonitor -> Starts Agent Monitor
* apiary-sting        -> Starts Sting 
* apiary-timemachine  -> Starts Timemachine 
* apiary-pheromone    -> Starts Pheromone

Test Scripts
------------

Unit test suite to come...

Troubleshooting
---------------

##### Python says it can't find develop
You may need to install setuptools. To do that run "python ez\_setup.py". Or install it from your reposititory manager.

##### ./install.sh errors. 
You may have missing dependencies, make sure you install gcc, g++, make, ant, openjdk-7-jdk and python-dev.

Libraries Used and their Licenses 
--------------

* Configobj - BSD License - http://www.voidspace.org.uk/python/configobj.html
* pika - MPL License - https://github.com/pika/pika/
* pymongo - Apache v2.0 - https://github.com/mongodb/mongo-python-driver 
* jsonschema - No License listed - https://github.com/Julian/jsonschema
* pyLucene - Apache v2.0 - http://lucene.apache.org/pylucene/

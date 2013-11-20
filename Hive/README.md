The Hive
========

The middleware for the Apiary stack.

Components
----------

AgentManager, AgentMonitor - These components manage the connection and configuration of agents. 

Honeycomb - Controls insertion and collection of data from the database software via an API.

Install and Test
----------------

* run "python setup.py develop" to install the Hive binarys in development mode 
* Run start.sh to begin all the services in a screen session.
* Or run the Binaries defined below
* Run stop.sh to end the screen session created by start.sh

Current Binarys
---------------

* apiary-honeycomb -> Starts Honeycomb server
* apiary-agentmanager -> Starts Agent Manager
* apiary-agentmonitor -> Starts Agent Monitor

Test Scripts
------------

Unit test suite to come...

Requirements
------------

If running "python setup.py develop" doesn't work for you, you may need to installed setuptools. To do that run "python ez\_setup.py". 

Libraries Used and their Licenses 
--------------

* Configobj - BSD License - http://www.voidspace.org.uk/python/configobj.html
* pika - MPL License - https://github.com/pika/pika/
* pymongo - 

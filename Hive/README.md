The Hive
========

The middleware for the Apiary stack. 

The Hive is several services linked together by a central management service, communication between Hive components is by Message Bus

Components
----------

Control - The Center of the Hive, handles the bulk of the logic to do with the Hive.

Database - Controls insertion and collection of data from the database software via an API.

Intelligence - The Hive component that manages the map reduce etc..... via API


Install and Test
----------------

* run "python setup.py develop" to install the Hive binarys in development mode 
* Binarys are defined in the setup.py file under entry points.

Current Binarys
---------------

* apiary_honeycomb -> Starts Honeycomb server
* apiary_control -> Starts Control Server
* apiary-intelligence -> Starts Intelligence Server

Test Scripts
------------

* fire\_test\_message.py - Sends a correct XML message onto the Honeycomb Work Queue
* fire\_bad\_test\_message.py - Sends a message with an incorrect Action to Honeycomb 

Requirements
------------

If installing and you run into issues building you may need to install: libxml2-dev, libxslt-dev and python-dev 

On debian: 
* sudo apt-get install -y libxslt-dev libxml2-dev python-dev 
  

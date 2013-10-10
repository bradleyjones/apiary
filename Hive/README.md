The Hive
========

The middleware for the Apiary stack. 

The Hive is several services linked together by a central management service, communication between Hive components is by Message Bus

Components
----------

Control - The Center of the Hive, this component connects all the other Hive parts together.

Database - Controls insertion and collection of data from the database software via an API.

REST - A REST API for application layer comunication to the Hive e.g. the front end.

Intelligence - The Hive component that manages the map reduce etc..... via API

Install and Test
----------------

* run "python setup.py develop" to install the Hive binarys in development mode 
* Binarys are defined in the setup.py file under entry points.

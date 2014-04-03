The Queen Bee
========

The Apiary dashboard, provides and interface for analytics and advanced querying of Apiary components

Requirements
========

Mongodb is used to store sessions as well as user and project info. You will need to have mongodb installed on your system and running before you can use the dashboard.

To start mongodb if it is not running:

````sudo mongod````

Node packages: express, jade, socket.io, amqp, crypto, mongoose, connect-mongo, bcrypt, colors, cookie, connect

To get started run from within the Queen directory:

````npm install````

to install all the dependencies followed by

````node server.js````

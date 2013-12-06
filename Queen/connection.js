var config = require('./config/config')
  , amqp = require('amqp')
  , connection = {};

connection._conn = amqp.createConnection({host: config.rabbitIP});

connection.dataCache = {
  agents: {}
};

module.exports = connection;

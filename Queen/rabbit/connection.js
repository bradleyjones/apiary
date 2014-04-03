/*
 * Create a connection to the rabbitmq server
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

var config = require('../config/config')
  , amqp = require('amqp')
  , connection = {};

connection._conn = amqp.createConnection({host: config.rabbitIP});

connection.dataCache = {
  agents: {}
};

module.exports = connection;

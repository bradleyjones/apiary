/*
 * Create a new RPC (Remote Procedure Call) Query
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

"use strict";

var config = require('../config/config')
  , amqp = require('amqp')
  , crypto = require('crypto')
  , CONTENT_TYPE = 'application/json'
  , colors = require('colors')
  , connection = require('./connection')._conn;

//New RPC query
exports.RPCQuery = function (queueName, data, callback) {
  var self = this;

  self.responseQueue = false;
  self.correlationId = crypto.randomBytes(16).toString('hex');

  connection.queue('', {exclusive: true}, function (queue) {
    self.responseQueue = queue.name;
    queue.subscribe(function (message, headers, deliveryInfo, m) {
      try {
        if (self.correlationId === m.correlationId) {
          var msg = message['data'].toString('utf-8');
          callback(JSON.parse(msg));
        }
      } catch(err) {
        throw err;
        console.log("Some Error Occured: ".red + err.red);
        return
      }
    });

    connection.publish(queueName, data, {
      correlationId: self.correlationId,
      contentType: CONTENT_TYPE,
      replyTo: self.responseQueue
    });
  });
};

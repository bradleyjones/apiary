/*
 * Create a new Publish/Subscribe connection on an exchange
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
  , sys = require('sys')
  , colors = require('colors')
  , connection = require('./connection')._conn;

exports.PubSub = function (exchangeName, routingKey, callback) {
    console.log("Creating Subscribe on exchange ".green + exchangeName.green +
        " routing key ".green + routingKey.green);

    connection.queue('', {exclusive: true}, function(queue) {
      queue.bind(exchangeName, routingKey);
      queue.subscribe(function(message, headers, deliveryInfo) {
        try {
          var msg = message['data'].toString('utf-8');
          console.log(JSON.parse(msg));
          callback(JSON.parse(msg));
        } catch(err) {
          console.log("There was an error: ".red + err.red);
          return
        }
      })
    });
};

"use strict";

var config = require('../config/config')
  , amqp = require('amqp')
  , crypto = require('crypto')
  , sys = require('sys')
  , colors = require('colors');

exports.PubSub = function (exchangeName, routingKey, callback) {
    var connection = amqp.createConnection({host: config.hiveIP}),
        self = this;

    connection.on('ready', onReady(connection, exchangeName, routingKey, callback));
    connection.on('error', function(e) {
      throw e;
    });
};

function onReady(connection, name, routingKey, callback) {
    return function() {
        console.log("connected to ".green + connection.serverProperties.product.green);
        // There is no need to declare type, 'topic' is the default:
        //var exchange = connection.exchange(name);

        connection.queue('', {exclusive: true}, onQueueCreateOk(name, routingKey, callback));
    }
}

function onQueueCreateOk(exchange, routingKey, callback) {
    return function(queue) {
        queue.bind(exchange, routingKey);
        queue.subscribe(onMessage(callback));
    }
}

function onMessage(callback) {
    console.log("on message")
    return function(message, headers, deliveryInfo) {
        try {
            var msg = message['data'].toString('utf-8');
            console.log(JSON.parse(msg));
            callback(JSON.parse(msg));
        } catch(err) {
            console.log("There was an error: ".red + err.red);
            return
        }
    }
}

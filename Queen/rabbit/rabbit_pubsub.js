"use strict";

var config = require('../config/config');
var amqp = require('amqp');
var crypto = require('crypto');
var sys = require('sys');

var TIMEOUT = 2000; //ms time to wait
var CONTENT_TYPE = 'application/json';

exports.PubSub = function (exchangeName, routingKey, callback) {
    var connection = amqp.createConnection({host: config.hiveIP}),
        self = this;

    connection.on('ready', onReady(connection, exchangeName, routingKey, callback));
};

function onReady(connection, name, routingKey, callback) {
    return function() {
        console.log("connected to " + connection.serverProperties.product);
        // There is no need to declare type, 'topic' is the default:
        console.log("Setting Up Exchange");
        var exchange = connection.exchange(name);
   
        console.log("Setting Up Queue");
        connection.queue('', {exclusive: true}, onQueueCreateOk(exchange, routingKey, callback));
    }
}

function onQueueCreateOk(exchange, routingKey, callback) {
    return function(queue) {
        console.log("Binding queue to routingKey " + routingKey);
        queue.bind(exchange, routingKey);
        console.log("Subscribing to queue");
        queue.subscribe(onMessage(callback));
        console.log("Listening...");
    }
}

function onMessage(callback) {
    return function(message, headers, deliveryInfo) {
        console.log("Message Received! Parsing...");
        var msg = message['data'].toString('utf-8');
        console.log(msg);
        console.log(JSON.parse(msg));
        callback(JSON.parse(msg));
    }
}

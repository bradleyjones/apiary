/*
 * Abstracted functions to make it easier to create new RPC (Remote Procedure
 * Call) and Publish/Subscribe connections to rabbit queues elsewhere in the
 * code in order to best keep to DRY (Don't Repeat Yourself) principles
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

"use strict";

var rpc = require('./rabbit_rpc')
  , pubsub = require('./rabbit_pubsub');

exports.constructMessage = function (action, queueName, data) {
    if (typeof (data) === 'undefined') {
        data = {};
    } ;
    var message = {
            action: action,
            data: data,
            to: queueName,
            machineid: '',
            from: 'Queen'
        };
    return message;
};

exports.constructQuery = function (action, queueName, data) {
    if (typeof (data) === 'undefined') {
        data = {};
    } ;
    var message = {
            action: action,
            data: {"QUERY" : data, "TIMESCALE" : 900000000000},
            to: queueName,
            machineid: '',
            from: 'Queen'
        };
    return message;
};

exports.rpc = function (queueName, data, callback) {
    rpc.RPCQuery(queueName, data, function (message) {
        callback(message);
    });
};

exports.pubsub = function (exchangeName, topic, callback) {
    pubsub.PubSub(exchangeName, topic, function (message) {
        console.log("PUBSUB: ", message);
        callback(message);
    });
};

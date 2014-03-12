"use strict";

var rpc = require('./rabbit_rpc')
  , pubsub = require('./rabbit_pubsub')

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

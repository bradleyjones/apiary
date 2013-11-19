"use strict";

var config = require('../config/config')
  , amqp = require('amqp')
  , crypto = require('crypto')
  , TIMEOUT = 4000 //ms time to wait
  , CONTENT_TYPE = 'application/json'
  , colors = require('colors');

//New RPC query
exports.RPCQuery = function (queueName, data, callback) {
    var connection = amqp.createConnection({host: config.hiveIP}),
        self = this;

    self.responseQueue = false;
    connection.on("ready", function () {
        self.correlationId = crypto.randomBytes(16).toString('hex');
        var timeout = setTimeout(function (corr_id) {
                console.error(new Error("timeout " + corr_id).red);
                //connection.end();
            }, TIMEOUT, self.correlationId);

        connection.queue('', {exclusive: true}, function (queue) {
            self.responseQueue = queue.name;
            queue.subscribe(function (message, headers, deliveryInfo, m) {
                try {
                    if (self.correlationId === m.correlationId) {
                        clearTimeout(timeout);
                        connection.end();
                        var msg = message['data'].toString('utf-8');
                        callback(JSON.parse(msg));
                    }
                } catch(err) {
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
    });
};


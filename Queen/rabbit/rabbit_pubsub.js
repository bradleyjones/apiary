var config = require('../config/config')
var amqp = require('amqp')
var crypto = require('crypto')
var sys = require('sys')

var TIMEOUT=2000; //ms time to wait
var CONTENT_TYPE='application/json';

exports.PubSub = function(queueName, data, callback){
  connection = amqp.createConnection({host:config.hiveIP});

  connection.on('ready', function () {
    console.log("connected to " + connection.serverProperties.product);
    // There is no need to declare type, 'topic' is the default:
    var exchange = connection.exchange('events');

    // Consumer:
    connection.queue('topic_queue',{}, function(queue){
      queue.bind(exchange, "agents");
      queue.subscribe(function (message) {
        // Get original message string:
        console.log(message.data.toString('ascii', 0, message.data.length));
      });
    });
  });
};

exports.PubSub()

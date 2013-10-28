var config = require('../config/config')
var amqp = require('amqp')
var crypto = require('crypto')
var sys = require('sys')

var TIMEOUT=2000; //ms time to wait
var CONTENT_TYPE='application/json';

exports.PubSub = function(exchangeName, topic, callback){
  connection = amqp.createConnection({host:config.hiveIP});
  var self = this
  self.exchangeName = exchangeName
  self.topic = topic
  self.callback = callback

  connection.on('ready', function () {
    console.log("connected to " + connection.serverProperties.product);
    // There is no need to declare type, 'topic' is the default:
    var exchange = connection.exchange(self.exchangeName);

    // Consumer:
    connection.queue('',{exclusive:true}, function(queue){
      queue.bind(exchange, self.topic);
      queue.subscribe(function (message) {
        // Get original message string:
        console.log(JSON.parse(message));
        self.callback(JSON.parse(JSON.parse(message)))
      });
    });
  });
};

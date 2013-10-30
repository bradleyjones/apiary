var config = require('../config/config')
var amqp = require('amqp')
var crypto = require('crypto')

var TIMEOUT=2000; //ms time to wait
var CONTENT_TYPE='application/json';

//New RPC query
exports.RPCQuery = function(queueName, data, callback){
  var connection = amqp.createConnection({host:config.hiveIP})
  var self = this;
  self.responseQueue = false;
  connection.on("ready", function(){
    self.correlationId = crypto.randomBytes(16).toString('hex');
    var timeout = setTimeout(function(corr_id){
      console.error(new Error("timeout " + corr_id));
      connection.end()
      }, TIMEOUT, self.correlationId);

    connection.queue('', {exclusive: true}, function(queue){
      self.responseQueue = queue.name;
      queue.subscribe(function(message, headers, deliveryInfo, m){
        if(self.correlationId = m.correlationId){
          clearTimeout(timeout)
          connection.end()
          callback(JSON.parse(message.data))
        }
      })
      connection.publish(queueName, data, {
        correlationId:self.correlationId,
        contentType:CONTENT_TYPE,
        replyTo:self.responseQueue
      })
    })

  });
};


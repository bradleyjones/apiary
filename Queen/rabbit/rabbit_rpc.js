var config = require('./config/config')
var amqp = require('amqp')
var crypto = require('crypto')

var TIMEOUT=2000; //ms time to wait
var CONTENT_TYPE='application/json';

//New RPC query
exports.RPCQuery = function(queueName, data, callback){
  var connection = amqp.createConnection({host:config.hiveIP})
  if(data == null){
    data = "<?xml version='1.0' encoding='utf8'?><message><action>AGENTS</action>action><to>Control</to>to><from>Unidentified</from>from><data>70:56:81:9b:0e:3b</data>data><machineid>70:56:81:9b:0e:3b</machineid>machineid></message>message>"
  }
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
          callback(message)
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


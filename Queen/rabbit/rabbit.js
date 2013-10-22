var rpc = require('./rabbit_rpc')
var pubsub = require('./rabbit_pubsub')
var parseXML = require('xml2js').parseString

exports.constructMessage = function(action, queueName, data){
  message = ""+
    "<?xml version='1.0' encoding='utf8'?>" +
    "<message>" +
      "<action>"+ action +"</action>" +
      "<to>" + queueName + "</to>" +
      "<from>Queen</from>" +
      "<data>" + data + "</data>" +
      "<machineid></machineid>" +
    "</message>";

  return message;
}

exports.getData = function(message){
  data = null
  parseXML(message, {explicitArray: false}, function(err, result){
    if(err) { console.log(err) }
    else{
      data = result
    }
  })
  console.log("DATA: ", data)
  return data
}

exports.rpc = function(queueName, data, callback){
  rpc.RPCQuery(queueName, data, function(message){
    var data = exports.getData(message)
    var data2 = exports.getData(data.message.data)
    callback(data2)
  })
}

exports.pubsub = function(exchangeName, topic, callback){
  pubsub.PubSub(exchangeName, topic, function(message){
    var data = exports.getData(message)
    console.log("PUBSUB: ", data)
    callback(data)
  })
}

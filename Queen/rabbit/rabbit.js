var rpc = require('./rabbit_rpc')
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
  console.log("message: ", message)
  data = null
  parseXML(message, function(err, result){
    parseXML(result.message.data[0], function(err2, result2){
      console.log(data)
      data = result2
    })
  })
  return data
}

exports.rpc = function(queueName, data, callback){
  rpc.RPCQuery(queueName, data, callback)
}

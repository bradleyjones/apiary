var rpc = require('./rabbit_rpc')

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

exports.rpc = function(queueName, data, callback){
  rpc.RPCQuery(queueName, data, callback)
}

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
  data = null
  parseXML(message, {explicitArray: false}, function(err, result){
    if(err) { console.log(err) }
    else{
      console.log(result.message.data)
      parseXML(result.message.data, {explicitArray:false}, function(err2, result2){
        if(err2) { console.log(err) }
        else{
          console.log(result2)
          data = result2
        }
      })
    }
  })
  console.log("DATA: ", data)
  return data
}

exports.rpc = function(queueName, data, callback){
  rpc.RPCQuery(queueName, data, callback)
}

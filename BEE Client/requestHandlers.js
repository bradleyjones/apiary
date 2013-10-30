/*
  Request Handlers
  Main application behavior defined here
*/


//Libraries
var fs = require('fs');
var amqp = require ('amqp');
var config = require('./config')

/*
  Initialise
  Takes response from initial handshake and handles data.
*/
function initialise(messageData){
  console.log("Setting client ID:");
  config.clientID = messageData.data;
  console.log(config.clientID);
  console.log("Initialisation Complete.");
}

/*
  Heatbeat handler
*/
function heartbeat(messageData){

  pushOntoMessageBus("Control", "control", "HEARTBEAT", "");
  console.log("----^----");
}


/*
  AddTarget
  Adds a new target file, and starts an asynchronous watch process
  Watch process dumps logs onto Message Bus once received.
*/
function addTarget(messageData) {
  file = messageData.data;
  console.log("Logging - " + file);
  
  if (config.hiveIP == 0) {
    throwError("ERROR - Bee not initialised, no Hive address.", messageData);
  } else if (file == null){
    throwError("ERROR - No Bee target specified.", messageData);
  } else if (!fs.statSync(file).isFile()){
    throwError("ERROR - Bee target file not found.", messageData);  // Not functioning Need to properly catch exception, possibly further down   
  } else {
    
    startByte = 0;
    
    //Set Starting Byte to the end of the file
    fs.stat(file, function(error, stats){
      if (error) throw error;
      startByte = stats.size;
    });
    
    //Watch File
    fs.watchFile(file, {persistent: true}, function(current, previous){
      console.log(file + " was modified");
      
      //On event, read in new bytes.
      fs.stat(file, function(error, stats){
        if (error) throw error;
        fs.createReadStream(file, {
          encoding: 'ascii',
          start: startByte,
          end: stats.size
        }).addListener("data", function(lines) {
          console.log(lines);
          pushOntoMessageBus(lines, config.hiveIP);//Push onto Message Bus
          startByte = stats.size;
        });
      });
    });
  }
}

/*
  RemoveTarget
  Will cease watching of specificed file. Not implemented.
  Probably need to keep watch processes in a Field Variable.
*/
function removeTarget(messageData) {
  console.log("Removing Target");
}


/* 
  Helper Function - Error Response
*/
function throwError(message, data){
  console.log(message)
  console.log(data);

  pushOntoMessageBus("Control", "Error", "ERROR", message + data); 
}

/*
  Helper Function - Push to MessageBus
*/
function pushOntoMessageBus(to, queue, action, data){
  
  //Start connection
  var connection = amqp.createConnection
  (
    {host: config.hiveIP} // Set to config file
  );
  
  //On connection push message
  connection.on
  (
    'ready', 
     function()
     {

     message = {
            action: action,
            to: to,
            from: config.clientID,
            data: data,
            machineid: config.macAddress
     }
          
     connection.publish(queue, message,{replyTo: config.queueName, correlationId: config.uuid});
     console.log("Sent message: ");
     console.log(message);
     connection.end();
     }
  );
}

//Expose functions for Router
exports.initialise = initialise;
exports.addTarget = addTarget;
exports.removeTarget = removeTarget;
exports.heartbeat = heartbeat;








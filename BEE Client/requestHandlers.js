/*
  Request Handlers
  Main application behavior defined here
*/


//Libraries
var fs = require('fs');
var amqp = require ('amqp');
var config = require('./config')

//global
var clientUUID = ""; 

/*
  Initialise
  Takes response from initial handshake and handles data.
*/
function initialise(response){
  config.clientID = response.data;
  console.log(config.clientID);
  console.log("Initialisation Complete.");
}



/*
  AddTarget
  Adds a new target file, and starts an asynchronous watch process
  Watch process dumps logs onto Message Bus once received.
*/
function addTarget(response) {
  file = response;
  console.log("Logging - " + file);
  
  if (config.hiveIP == 0) {
    throwError("ERROR - Bee not initialised, no Hive address.", response);
  } else if (file == null){
    throwError("ERROR - No Bee target specified.", response);
  } else if (!fs.statSync(file).isFile()){
    throwError("ERROR - Bee target file not found.", response);  // Not functioning Need to properly catch exception, possibly further down   
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
function removeTarget(response) {
  console.log("Removing Target");
}


/* 
  Helper Function - Error Response
*/
function throwError(message, response){
  console.log(message)
  response.writeHead(500, {"Content-Type": "text/plain"});
  response.write(message);
  response.end();
}

/*
  Helper Function - Push to MessageBus
*/
function pushOntoMessageBus(message, hiveIP){
  
  //Open Rabbit Connection
  var connection = amqp.createConnection
  (
    {host: hiveIP}
  );
  
  //On connection push message
  connection.on
  (
    'ready', 
    function()
    {
      var queueToSendTo = "testMessageQueue";

      connection.publish
      (
        queueToSendTo, 
        message
      );

      console.log
      (
        "Sent message: "
        + message
      );
    }
  );
}

//Expose functions for Router
exports.initialise = initialise;
exports.addTarget = addTarget;
exports.removeTarget = removeTarget;








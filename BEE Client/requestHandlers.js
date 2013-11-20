/*
  Request Handlers
  Main application behavior defined here
*/


//Libraries
var fs = require('fs');
var amqp = require ('amqp');
var config = require('./config')

//Field Variables
var interval = {};
var fileWatchers = [];
var heartbeatFunction = function(){ // possibly just make normal function
  pushOntoMessageBus("Control", "agents."+config.clientID+".heartbeat", "HEARTBEAT", "Beat", "apiary");
  console.log("----^----");
};

/*
  Initialise
  Takes response from initial handshake and handles data.
*/
function initialise(messageData){

  if(config.heartbeatInterval == undefined){
    console.log ("No heatbeat interval defined, update config file.");
    process.exit(1);
  }

  console.log("Setting client ID:");
  config.clientID = messageData.data;
  console.log(config.clientID);
  console.log("Initialisation Complete.");

  //Start heartbeat interval
  interval = setInterval(heartbeatFunction, config.heartbeatInterval);
}

/*
  AddTarget
  Adds a new target file, and starts an asynchronous watch process
  Watch process dumps logs onto Message Bus once received.
*/
function setFiles(messageData) {

  //Parse FileList
  fileList = messageData.data;
  console.log("Logging - " + file);

  for(file in fileList){
    filename = fileList[file];  
    
    var watcher = function (){

      var startByte = 0;
    
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
            pushOntoMessageBus("honeyComb","agents."+config.clientID+".data","dataInput",lines,"apiary");//Push onto Message Bus
            startByte = stats.size;
  
            //Reset Interval Timer 
            clearInterval(interval);
            interval = setInterval(heartbeatFunction, config.heartbeatInterval);
          });
        });
      });
    }
    fileWatchers.push(watcher);
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
function pushOntoMessageBus(to, queueToSendTo, action, data, exchangeName){
    
    //Construct Message
    message = {
                action: action,
                to: to,
                from: config.clientID,
                data: data,
                machineid: config.macAddress
        }

    //If no exchange defined, push onto default the old way
    //Consider legacy, possibly remove.
    if (exchangeName == undefined){
        config.connection.publish(queueToSendTo, message, {correlationId: config.cID});   
    } else {
        var exchange = config.connection.exchange(exchangeName);
        try {
            exchange.publish(queueToSendTo, message, {correlationId: config.cID});       
        } catch (err) {
            console.log(err);
        }
    }

    console.log("Sent message: ");
    console.log(message);
    console.log("On Queue : " +queueToSendTo);
}

//Expose functions for Router
exports.initialise = initialise;
exports.setFiles = setFiles;
exports.removeTarget = removeTarget;








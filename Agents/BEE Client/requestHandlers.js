/*
 * Request Handlers
 * Main application behavior defined here
 *
 * __author__ = "Jack Fletcher, Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */


//Libraries
var fs = require('fs');
var amqp = require ('amqp');
var fileListener = require ('./fileListener');
var config = require('./config');

//Field Variables
var interval = {};
var fileWatchers = [];
var heartbeatFunction = function(){ // possibly just make normal function
  pushOntoMessageBus("AgentManager", "agents."+config.clientID+".heartbeat", "HEARTBEAT", {}, "apiary");
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
  fileList = messageData.data.files;

  for(file in fileList){
    filename = fileList[file].path;
    console.log('Logging - ' + filename);
    tags = fileList[file].tags;
    
    callback = function(lines){
      console.log(lines);

      //Construct Message
      payload = {
        'CONTENT':lines,
        'TYPE':"file",
        'EVENTTIMESTAMP': new Date().getTime().toString(),
        'METADATA': {
              'FILENAME':filename,
              'AGENT': config.clientID,
              'TAGS':tags
            }
      };
    
      //Push onto bus
      pushOntoMessageBus("HoneyComb","agents."+config.clientID+".data","DATA",payload,"apiary");
  
      //Reset Interval Timer 
      clearInterval(interval);
      interval = setInterval(heartbeatFunction, config.heartbeatInterval);
    }

    //Create file watcher and push onto list of watchers.
    fileWatchers.push(fileListener.watchFile(filename, callback));
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

function receivedError(messageData) {
  console.log("RECEIVED ERROR");
  console.log(messageData);
  console.log(messageData.data);
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

    try {
        //If no exchange defined, push onto default the old way
        //Consider legacy, possibly remove.
        if (exchangeName == undefined){
            config.connection.publish(queueToSendTo, message);   
        } else {
          var eAS = config.connection.exchange(exchangeName, {noDeclare:true})
          eAS.publish(queueToSendTo, message, {});       
          console.log("Sent message: ");
          console.log(message);
          console.log("On Queue : " +queueToSendTo);
        }
    } catch (err) {
        console.log(err);
    }
}

//Expose functions for Router
exports.initialise = initialise;
exports.setFiles = setFiles;
exports.removeTarget = removeTarget;
exports.receivedError = receivedError;

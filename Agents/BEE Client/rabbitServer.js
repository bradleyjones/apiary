/*
  Server.js - Main Server Setup process
*/

//Libraries
var amqp = require('amqp');
var config = require('./config');
var getMac = require('getmac');

//Start Rabbit Server
function start(route, handle) {

  console.log("BEE has started.");

  if(config.hiveIP == undefined){
    console.log ("No hive locator, update config file.");
    process.exit(1);
  }

  //Start Server
  config.connection = amqp.createConnection
  (
  	{host: config.hiveIP} // Set to config file
  );

  //Once connection up
  config.connection.on
  ('ready', function(){

    //Set receive queue
    config.connection.queue("",
  		{autoDelete: false,
       durable: true,
       exclusive: true}, 
       function(queue){

         //Queue ready to recieve, so alert Hive
         alertHive(queue.name, config.hiveIP);
         console.log('Waiting for messages...');
              
         //Subscribe
         queue.subscribe(

           //Action on message Received
  	   function(messageReceived){
             data = JSON.parse(messageReceived.data);  

             console.log("Request for " + data.action + " received.");
             //Forward to Router
             route(handle, data.action, data); 
          
  	   }  
         )
       }
     )
  });
}

//
//  Helper Function - Initial Hive alert
//
function alertHive(queueName, hiveIP){

  //Get Systems Mac Address for ID purpose.  
  getMac.getMac(function(err,macAddress){
      if (err)  throw err;

      //Set macAddress global
      config.macAddress = macAddress;

      //TODO Check if ID already present, could be preinitialised machine reconnecting.      

      var queueToSendTo = "agentmanager";
      config.cID = generateUUID();          

      message = {
        action: "HANDSHAKE",
        to: "AgentManager",
        from: "Unidentified",
        data: "",
        machineid: config.macAddress
      }
          
      config.connection.publish(queueToSendTo, message,{replyTo: queueName});
      console.log("Sent message: ");
      console.log(message);      
  });
}

/*
  UUID Generator, for rabbitmq correlationID and right now machineID
*/
function generateUUID(){
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
    return v.toString(16);
  });
}

exports.start = start;

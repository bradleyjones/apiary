/*
  Server.js - Main Server Setup process
*/

//Libraries
var http = require("http");
var url = require("url");
var amqp = require('amqp');
var config = require('./config');
var getMac = require('getmac');

//Start Rabbit Server
function start(route, handle) {

  console.log("BEE has started.");

  //Start Server
  var connection = amqp.createConnection
  (
  	{host: config.hiveIP} // Set to config file
  );

  //Once connection up
  connection.on
  ('ready', function(){

    //Set receive queue
  	connection.queue("", 
  		{autoDelete: false,
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
      console.log(macAddress);       
      console.log(hiveIP);
      
      //Start Server
      var connection = amqp.createConnection
      (
      	{host: hiveIP} // Set to config file
      );
  
      //On connection push message
      connection.on
      (
        'ready', 
        function()
        {
          var queueToSendTo = "control";
          uuid = generateUUID();          

          message = {
            action: "HANDSHAKE",
            to: "Control",
            from: "Unidentified",
            data: "",
            machineid: macAddress
          }
          
          connection.publish(queueToSendTo, message,{replyTo: queueName, correlationId: uuid});
          console.log("Sent message: ");
          console.log(message);
        }
      );       
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

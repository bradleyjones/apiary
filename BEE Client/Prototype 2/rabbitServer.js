/*
  Server.js - Main Server Setup process
*/

//Libraries
var http = require("http");
var url = require("url");
var amqp = require('amqp');
var xmlParse = require('xml2js').parseString;

//Start Rabbit Server
function start(route, handle) {

  //Start Server
  var connection = amqp.createConnection
  (
  	{host: 'localhost'} // Set to config file
  );

  //Set Queue
  var queueToReceiveFrom = "testMessageQueue"; //Set to config file

  //Once connection up
  connection.on
  ('ready', function(){
    
    //Set receive queue
  	connection.queue(
  	  queueToReceiveFrom, 
  		{autoDelete: false}, 
  		function(queue){
  			console.log('Waiting for messages...');
        
        //Subscribe
  			queue.subscribe(
          //Action on message Received
  				function(messageReceived){
              
            data = messageReceived.data.toString();
              
            xmlParse(data, function(err, result){
              console.log("Request for " + result.action + " received.");
                
              //Send to Router
              route(handle, result.action, result);
            });
  			  }
  			);
  		}
  	);
  });
  
  console.log("BEE has started.");
}

exports.start = start;
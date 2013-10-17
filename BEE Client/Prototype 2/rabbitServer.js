/*
  Server.js - Main Server Setup process
*/

//Libraries
var http = require("http");
var url = require("url");
var amqp = require('amqp');
var config = require('./config');
var getMac = require('getMac');
var xmlParse = require('xml2js').parseString;

//Start Rabbit Server
function start(route, handle) {

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
        
        alertHive(queue.name, config.hiveIP)
        
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
            })
  			  }  
  			)
  		}
  	)
  });
  console.log("BEE has started.");
}

//
//  Helper Function - Push to MessageBus
//
function alertHive(queueName, hiveIP){
  
  getMac.getMac(function(err,macAddress){
      if (err)  throw err;
      console.log(macAddress);  
      
      console.log(hiveIP);
      
      var UUID = Date.now();
      
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
          
          message = ""+
          "<xml>" +
          "<message>" +
            "<to>Control</to>" +
            "<from>Unidentified</from>" +
            "<machineid>"+ macAddress +"</machineid>" +
            "<action>HANDSHAKE</action>" +
            "<data>"+ macAddress +"</data>" +
          "</message>" +
          "</xml>";
          
          connection.publish(queueToSendTo, message,{replyTo: queueName, correlationId: UUID});
          
          console.log("Sent message: "+ message);
        }
      );       
  });
}

exports.start = start;
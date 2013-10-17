#
#  Server.js - Main Server Setup process
#

#Start Rabbit Server
start = (route, handle) ->
  
  #Start Server
  connection = amqp.createConnection(host: config.hiveIP) # Set to config file
  
  #Set Queue
  queueToReceiveFrom = "testMessageQueue" #Set to config file
  
  #Once connection up
  connection.on ("ready") ->
    
    #Set receive queue
    connection.queue queueToReceiveFrom,
      autoDelete: false
    , (queue) ->
      console.log "Waiting for messages..."
      
      #Subscribe
      queue.subscribe (messageReceived) ->
        #Action on message Received
        data = messageReceived.data.toString()
        xmlParse data, (err, result) ->
          console.log "Request for " + result.action + " received."
          
          #Send to Router
          route (handle, result.action, result)
      
      #Notify Hive that im alive
      alertHive config.hiveIP

  console.log "BEE has started."
  
#
#  Helper Function - Push to MessageBus
#
alertHive = (hiveIP) ->
  
  #Open Rabbit Connection
  connection = amqp.createConnection(host: hiveIP)
  
  #On connection push message
  connection.on "ready", ->
    queueToSendTo = "control"
    connection.publish queueToSendTo, 
    console.log "Hey im up bitch"
  
#Libraries
http = require("http")
url = require("url")
amqp = require("amqp")
config = require("./config.js.coffee")
xmlParse = require("xml2js").parseString

#Export methods
exports.start = start
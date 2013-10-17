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
  connection.on "ready", ->
    
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
          route handle, result.action, result

  console.log "BEE has started."
  
#Libraries
http = require("http")
url = require("url")
amqp = require("amqp")
config = require("./config")
xmlParse = require("xml2js").parseString

#Export methods
exports.start = start
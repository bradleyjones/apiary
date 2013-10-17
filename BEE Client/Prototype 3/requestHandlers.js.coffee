#
#  Request Handlers
#  Main application behavior defined here
#

#
#  AddTarget
#  Adds a new target file, and starts an asynchronous watch process
#  Watch process dumps logs onto Message Bus once received.
#
addTarget = (response) ->
  file = response
  console.log "Logging - " + file
  if config.hiveIP is 0
    throwError "ERROR - Bee not initialised, no Hive address.", response
  else unless file?
    throwError "ERROR - No Bee target specified.", response
  else unless fs.statSync(file).isFile()
    throwError "ERROR - Bee target file not found.", response # Not functioning Need to properly catch exception, possibly further down
  else
    startByte = 0
    
    #Set Starting Byte to the end of the file
    fs.stat file, (error, stats) ->
      throw error  if error
      startByte = stats.size

    
    #Watch File
    fs.watchFile file,
      persistent: true
    , (current, previous) ->
      console.log file + " was modified"
      
      #On event, read in new bytes.
      fs.stat file, (error, stats) ->
        throw error  if error
        fs.createReadStream(file,
          encoding: "ascii"
          start: startByte
          end: stats.size
        ).addListener "data", (lines) ->
          console.log lines
          pushOntoMessageBus lines, config.hiveIP #Push onto Message Bus
          startByte = stats.size

#
#  RemoveTarget
#  Will cease watching of specificed file. Not implemented.
#  Probably need to keep watch processes in a Field Variable.
#
removeTarget = (response) ->
  console.log "Removing Target"

# 
#  Helper Function - Error Response
#
throwError = (message, response) ->
  console.log message
  response.writeHead 500,
    "Content-Type": "text/plain"

  response.write message
  response.end()

#
#  Helper Function - Push to MessageBus
#
pushOntoMessageBus = (message, hiveIP) ->
  
  #Open Rabbit Connection
  connection = amqp.createConnection(host: hiveIP)
  
  #On connection push message
  connection.on "ready", ->
    queueToSendTo = "testMessageQueue"
    connection.publish queueToSendTo, message
    console.log "Sent message: " + message

#Libraries
fs = require("fs")
amqp = require("amqp")
config = require("./config.js.coffee")

#Expose functions for Router
exports.addTarget = addTarget
exports.removeTarget = removeTarget

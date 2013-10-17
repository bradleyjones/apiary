amqp = require("amqp")
connection = amqp.createConnection(host: "localhost")
queueToReceiveFrom = "testMessageQueue"

connection.on "ready", ->
  connection.queue queueToReceiveFrom,
    autoDelete: false
  , (queue) ->
    console.log "Waiting for messages..."
    queue.subscribe (messageReceived) ->
      console.log "Received message: " + messageReceived.data.toString()



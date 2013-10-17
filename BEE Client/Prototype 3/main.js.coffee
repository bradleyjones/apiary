#
#  Main.js Starting point for BEE Client
#  Requires amqp 'npm install amqp'
#  Requires xml2js 'npm install xml2js'
#  Start with 'coffee main.js.coffee'
#

#Initialise Routes, Start Server
server = require("./rabbitServer.js.coffee")
router = require("./router.js.coffee")
requestHandlers = require("./requestHandlers.js.coffee")

handle = {}
addTarget = "addTarget"
handle[addTarget] = requestHandlers.addTarget
removeTarget = "removeTarget"
handle[removeTarget] = requestHandlers.removeTarget

server.start router.route, handle
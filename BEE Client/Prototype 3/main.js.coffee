#
#  Main.js Starting point for BEE Client
#  Requires amqp 'npm install amqp'
#  Requires xml2js 'npm install xml2js'
#  Start with 'coffee main.js.coffee'
#

#Initialise Routes, Start Server
server = require("./rabbitServer")
router = require("./router")
requestHandlers = require("./requestHandlers")

handle = {}
handle["addTarget"] = requestHandlers.addTarget
handle["removeTarget"] = requestHandlers.removeTarget

server.start router.route, handle
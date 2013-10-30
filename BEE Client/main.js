/*
  Main.js Starting point for BEE Client
  Requires amqp 'npm install amqp'
  Requires xml2js 'npm install xml2js'
  Requires getmac 'npm install getmac'
  Start with 'node main.js'
*/

//Initialise Routes, Start Server
var server = require("./rabbitServer");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["DONE"] = requestHandlers.initialise;
handle["HEARTBEAT"] = requestHandlers.heartbeat;
handle["addTarget"] = requestHandlers.addTarget;
handle["removeTarget"] = requestHandlers.removeTarget;

server.start(router.route, handle);

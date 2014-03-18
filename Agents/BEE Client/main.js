/*
  Main.js Starting point for BEE Client
  Requires amqp 'npm install amqp'
  Requires getmac 'npm install getmac'
  Start with 'node main.js'
*/

//Initialise Routes, Start Server
var server = require("./rabbitServer");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["DONE"] = requestHandlers.initialise;
handle["SETFILES"] = requestHandlers.setFiles;
handle["removeTarget"] = requestHandlers.removeTarget;
handle["Error"] = requestHandlers.receivedError;

server.start(router.route, handle);

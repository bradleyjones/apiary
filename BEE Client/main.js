//List Routes, Start Server

var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers")

var handle = {}
handle["/initialise"] = requestHandlers.initialise;
handle["/addTarget"] = requestHandlers.addTarget;
handle["/removeTarget"] = requestHandlers.removeTarget;

server.start(router.route, handle);
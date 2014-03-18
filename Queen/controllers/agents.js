"use strict";

var config = require('../config/config.js')
, rabbit = require('../rabbit/rabbit')
, init = require('../rabbit/init_subscribes')
, main = require('../server.js')
, io = main.io
, dataCache = require('../rabbit/connection').dataCache;

exports.list = function (req, res) {
  res.render('agents.jade');
};

exports.individual = function (req, res) {
  var msg = rabbit.constructMessage('SINGLEAGENT', 'agentmanager', req.params.id);
  new rabbit.rpc('agentmanager', msg, function (data) {
    var agent = data.data;
    if (agent !== null) {
      req.params.machineid = agent.machineid;
      res.render('agent.jade', agent);
    } else {
      res.send('NOT FOUND', 404);
    }
  });
};


// Web Sockets
io.of('/agents').on('connection', function (socket) {
  console.log("AGENTS");

  // Get the current number of connect agents
  socket.emit('init', dataCache.agents);

  // New agent added
  socket.on('newTarget', function (data) {
    console.log("adding new target");
    var msg = rabbit.constructMessage('SETFILES', 'agentmanager', data);
    new rabbit.rpc('agentmanager', msg, function (data) {
      console.log(data);
    });
  });

   //Agent gone offline
  //socket.on('agentOffline', function (id) {
    //socket.broadcast.emit('offline', id);
  //});
});

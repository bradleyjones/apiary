/*
 * Agents controller, controls loading the data/agents page and has serverside
 * code needed for websockets to configure agents
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

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
  // Get the current number of connect agents
  socket.emit('init', dataCache.agents);

  // Get the current tags
  var msg = rabbit.constructMessage('TAGS', 'honeycomb');
  new rabbit.rpc('honeycomb', msg, function(data) {
    console.log(data.data.TAGS);
    socket.emit('tags', data.data.TAGS);
  });

  // New agent added
  socket.on('newTarget', function (data) {
    console.log("adding new target");
    var msg = rabbit.constructMessage('SETFILES', 'agentmanager', data);
    console.log(msg);
    new rabbit.rpc('agentmanager', msg, function (data) {
      console.log(data);
    });
  });

  //Agent gone offline
  //socket.on('agentOffline', function (id) {
    //socket.broadcast.emit('offline', id);
  //});
});

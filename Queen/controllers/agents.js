"use strict";

var config = require('../config/config.js');
var rabbit = require('../rabbit/rabbit');
var main = require('../server.js');
var io = main.io;

exports.list = function (req, res) {
    res.render('agents.jade');
};

exports.individual = function (req, res) {
    var msg = rabbit.constructMessage('SINGLEAGENT', 'control', req.params.id);
    new rabbit.rpc('control', msg, function (data) {
        console.log("SINGLE: ", data);
        var agent = data.data;
        console.log(agent);
        if (agent !== null) {
            req.params.machineid = agent.machineid;
            res.render('agent.jade', agent);
        } else {
            res.send('NOT FOUND', 404);
        }
    });
};

function subscribeReady() {
    new rabbit.pubsub('events', 'control.agents', function (data) {
        io.sockets.emit('agent', data);
    });
}

subscribeReady();

// Web Sockets
io.sockets.on('connection', function (socket) {
    // Get the current number of connect agents
    msg = rabbit.constructMessage('ALLAGENTS', 'control');
    new rabbit.rpc('control', msg, function (data) {
        console.log("ADADASDASD", data);
        socket.emit('init', data);
    });

    // New agent added
    socket.on('newAgent', function (data) {
        socket.broadcast.emit('agent', data);
    });

    // Agent gone offline
    socket.on('agentOffline', function (id) {
        socket.broadcast.emit('offline', id);
    });
});

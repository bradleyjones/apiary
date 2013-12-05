// Home Page Controller

var rabbit = require('../rabbit/rabbit')
, main = require('../server.js')
, io = main.io;

exports.index = function (req, res) {
  var msg = rabbit.constructMessage('AGENTSCOUNT', 'agentmanager');
  new rabbit.rpc('agentmanager', msg, function (data) {
    console.log("AGENT COUNT ::: " + data.data)
  });

  res.render('home.jade');
};

// Web Sockets
io.sockets.on('connection', function (socket) {
  // Get the current number of connect agents
  var msg = rabbit.constructMessage('AGENTSCOUNT', 'agentmanager');
  new rabbit.rpc('agentmanager', msg, function (data) {
    console.log("AGENT COUNT ::: " + data.data);
    socket.emit('agentcount', data.data);
  });
});

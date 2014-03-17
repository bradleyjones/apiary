// Home Page Controller

var rabbit = require('../rabbit/rabbit')
, main = require('../server.js')
, io = main.io;

exports.index = function (req, res) {
  res.render('home.jade');
};

// Web Sockets
io.of('/home').on('connection', function (socket) {
  // Get the current number of connect agents
  var msg = rabbit.constructMessage('AGENTSCOUNT', 'agentmanager');
  new rabbit.rpc('agentmanager', msg, function (data) {
    console.log("AGENT COUNT ::: " + data.data);
    socket.emit('agentcount', data.data);
  });

  // Get the timestamps of all events
  var msg = rabbit.constructMessage('TIMESTAMPS', 'honeycomb');
  console.log(msg);
  new rabbit.rpc('honeycomb', msg, function (data) {
    console.log("TIMESTAMP DATA :::" + data.data);
    socket.emit('timestamps', data.data);
  });
});

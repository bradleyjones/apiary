exports.list = function(req, res){
  res.render('agents.jade')
}

// List of all agents
var allAgents = {};

// Web Sockets
io.sockets.on('connection', function (socket) {
  // Get the current number of connect agents
  socket.emit('init', allAgents);

  // New agent added
  socket.on('newAgent', function (data) {
    allAgents[data.id] = data;
    socket.broadcast.emit('agent', data);
  });

  // Agent gone offline
  socket.on('agentOffline', function (id) {
    delete allAgents[id];
    console.log(allAgents);
    socket.broadcast.emit('offline', id)
  });
});

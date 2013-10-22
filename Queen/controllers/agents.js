var rabbit = require('../rabbit/rabbit')

exports.list = function(req, res){
  res.render('agents.jade')
}

exports.individual = function(req, res){
  var agent = allAgents[req.params.id];
  if (agent != undefined) {
    res.render('agent.jade', agent);
  } else {
    res.send('NOT FOUND', 404);
  }
}

// Web Sockets
io.sockets.on('connection', function (socket) {
  // Get the current number of connect agents
  msg = rabbit.constructMessage('AGENTS','control')
  new rabbit.rpc('control',msg, function(data){
    socket.emit('init', rabbit.getData(data));
  })

  // New agent added
  socket.on('newAgent', function (data) {
    socket.broadcast.emit('agent', data);
  });

  // Agent gone offline
  socket.on('agentOffline', function (id) {
    socket.broadcast.emit('offline', id)
  });
});

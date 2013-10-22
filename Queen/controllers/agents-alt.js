var rabbit = require('../rabbit/rabbit')

// Get all the agents initially
msg = rabbit.constructMessage('ALLAGENTS','control')
var agents = {}
new rabbit.rpc('control',msg, function(data){
  agents = data
})

exports.list = function(req, res){
  res.render('agents.jade')
}

exports.individual = function(req, res){
  var agent = agents.agents[req.params.id];
  console.log(agent)
  if (agent != undefined) {
    req.params.machineid = agent.machineid
    res.render('agent.jade', agent);
  } else {
    res.send('NOT FOUND', 404);
  }
}

// Web Sockets
io.sockets.on('connection', function (socket) {
  // Get the current number of connect agents
  socket.emit('init', agents);

  // New agent added
  socket.on('newAgent', function (data) {
    socket.broadcast.emit('agent', data);
  });

  // Agent gone offline
  socket.on('agentOffline', function (id) {
    socket.broadcast.emit('offline', id)
  });
});

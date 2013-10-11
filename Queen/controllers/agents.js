exports.list = function(req, res){
  res.render('agents.jade')
}

// Web Sockets
io.sockets.on('connection', function (socket) {
  // Get the current number of connect agents
  socket.emit('init', { total: 200 });

  // New agent added
  socket.on('newAgent', function (data) {
    socket.broadcast.emit('agent', data);
  });
});

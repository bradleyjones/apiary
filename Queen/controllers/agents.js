exports.list = function(req, res){
  res.render('agents.jade')
}

// Web Sockets
io.sockets.on('connection', function (socket) {
  socket.on('newAgent', function (data) {
    socket.set('agent', data);
  });
});

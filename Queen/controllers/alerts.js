/*
 * Alerts Page Controller
 */

var rabbit = require('../rabbit/rabbit')
  , main = require('../server.js')
  , io = main.io;

exports.index = function (req, res) {
  res.render('alerts.jade');
};

/*
 * Sockets
 */
io.of('/alerts').on('connection', function(socket) {
  // Get session variables
  var sess = socket.handshake.session;
  socket.log.info('a socket with sessionID', socket.handshake.sessionID, 'connected');

  var userid = sess.user_id;


  socket.on('newalert', function(data) {
    console.log("setting up a new alert");

    // add user to the alert data object
    data.user = userid;

    var msg = rabbit.constructMessage('NEW', 'pheromone', data);
    new rabbit.rpc('pheromone', msg, function(resp) {
      console.log(resp);
    });
  })
})

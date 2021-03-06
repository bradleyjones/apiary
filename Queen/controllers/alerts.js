/*
 * Alerts Page Controller, controls loading the page and websockets to setup new
 * alerts
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
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

  // Get all current running alerts
  var msg = rabbit.constructMessage('ALL', 'pheromone');
  new rabbit.rpc('pheromone', msg, function(resp) {
    socket.emit('allalerts', resp.data);
  });

  socket.on('newalert', function(data) {
    console.log("setting up a new alert");

    // add user to the alert data object
    data.user = userid;

    var msg = rabbit.constructMessage('NEW', 'pheromone', data);
    new rabbit.rpc('pheromone', msg, function(resp) {
      console.log('successfully added new alert');

      socket.emit('added', resp.data);
    });
  })
})

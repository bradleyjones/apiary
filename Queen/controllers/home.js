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

    var timestamps = {};
    Object.keys(data.data).forEach( function (k) {
      var d = data.data[k];

      // Convert time to nearest 100 seconds
      var epochTime = d.EVENTTIMESTAMP;
      epochTime = Math.round(epochTime / 100) * 100;

      if (epochTime in timestamps) {
        timestamps[epochTime] += 1;
      } else {
        timestamps[epochTime] = 1;
      }
    });
    socket.emit('timestamps', timestamps);
  });
});

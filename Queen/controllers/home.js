/*
 * Home page controller, controls loading the home page and websockets for
 * getting information about the agents and system.
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
      epochTime = Math.round(epochTime / 10000) * 10000;

      if (epochTime in timestamps) {
        timestamps[epochTime] += 1;
      } else {
        timestamps[epochTime] = 1;
      }
    });
    socket.emit('timestamps', sortObject(timestamps));
  });
});

// Sort an object so that it is ordered by key
function sortObject(o) {
  var sorted = {}
    , a = [];

  for (key in o) {
    if (o.hasOwnProperty(key)) {
      a.push(key);
    }
  }

  a.sort();

  for (var key = 0; key < a.length; key++) {
    sorted[a[key]] = o[a[key]];
  }

  return sorted;
}

// Home Page Controller

var rabbit = require('../rabbit/rabbit')
, main = require('../server.js')
, io = main.io;

exports.index = function (req, res) {
  res.render('search.jade');
};

// Web Sockets
io.of('/search').on('connection', function (socket) {
  console.log("THIS BETTER WORK");

  socket.on("querySubmit", function(search) {
    console.log("Searching for term: " + search);

    var msg = rabbit.constructQuery('QUERY', 'honeycomb', search)
    new rabbit.rpc('honeycomb', msg, function (data) {
      console.log("TOTAL HITS RETURNED IS: " + data.data.totalhits);
      console.log("RETURNED DATA FROM QUERY IS: " + data.data.hits);

      socket.emit('results', data.data.hits)
    });
  });

  // Get the current tags
  var msg = rabbit.constructMessage('TAGS', 'honeycomb');
  new rabbit.rpc('honeycomb', msg, function(data) {
    console.log(data.data.TAGS);
    socket.emit('tags', data.data.TAGS);
  });
});

// Search Page Controller

var rabbit = require('../rabbit/rabbit')
, main = require('../server.js')
, io = main.io;

exports.index = function (req, res) {
  res.render('search.jade');
}

// Web Sockets
io.of('/search').on('connection', function (socket) {
  console.log("THIS BETTER WORK");

  // Get the current tags
  var msg = rabbit.constructMessage('TAGS', 'honeycomb');
  new rabbit.rpc('honeycomb', msg, function(data) {
    console.log(data.data.TAGS);
    socket.emit('tags', data.data.TAGS);
  });

  // Send the users saved searches


  // Submit new Query
  socket.on("querySubmit", function(search) {
    console.log("Searching for term: " + search);

    var msg = rabbit.constructQuery('QUERY', 'honeycomb', search)
    new rabbit.rpc('honeycomb', msg, function (data) {
      console.log("TOTAL HITS RETURNED IS: " + data.data.totalhits);
      console.log("RETURNED DATA FROM QUERY IS: " + data.data.hits);

      socket.emit('results', data.data.hits)
    });
  });

  // Save search
  socket.on('saveSearch', function(search) {
    console.log("Saving search: ", search);

    var userid = req.session.user_id;

    User.update({ _id: userid },
      {$push : {
            searches: search
          }},
      function(err) {
        if (err) {
          throw err;
        } else {
          console.log("Finished updating user searches");
        }
      });
  });
});

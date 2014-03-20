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
      console.log("TOTAL HITS RETURNED IS: " + data.data.totalHits);
      console.log("RETURNED DATA FROM QUERY IS: " + data.data.hits);

      socket.emit('results', data.data.hits);
    });
  });

  //HACK CODE, PLZ REMOVE
  socket.on("pieQuerySubmit", function(searches){
    console.log("Query for Pie Chart");
   
    runningResults = [];

    function recursiveQuery(searches, runningResults){
      console.log("Subseach Number" + searches.main.subsearch.length);
      if(searches.main.subsearch.length == 0){
        socket.emit('pieHackResults', runningResults);
      } else {
        console.log("Performing Search Iteration");
        //popSubSearch
        subsearch = searches.main.subsearch.pop();
        search = searches.main.search;
        //Append to searchi
        subsearchLabel = subsearch.label;
        subsearch = "("+search+") AND ("+subsearch.subQuery+")";

        //send to honeycomb
        var msg = rabbit.constructQuery('QUERY', 'honeycomb', subsearch)
        new rabbit.rpc('honeycomb', msg, function(data){
          console.log("TOTAL HITS RETURNED IS: " + data.data.totalHits);
          console.log("RETURNED DATA FROM QUERY IS: " + data.data.hits);

          runningResults.push({label: subsearchLabel, value: data.data.totalHits});
          recursiveQuery(searches, runningResults);
        });
      }
    }
    recursiveQuery(searches, runningResults);
  });

  // Get the current tags
  var msg = rabbit.constructMessage('TAGS', 'honeycomb');
  new rabbit.rpc('honeycomb', msg, function(data) {
    console.log(data.data.TAGS);
    socket.emit('tags', data.data.TAGS);
  });
});

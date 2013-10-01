//Server.js - Setup Server

var http = require("http");
var url = require("url");

//Start Server
function start(route, handle) {
  
  //Handle Request
  function onRequest(request, response) {
    var postData = "";
    var pathname = url.parse(request.url).pathname;
    
    console.log("Request for " + pathname + " received.");
    request.setEncoding("utf8");
    
    //Assemble Post Data
    request.addListener("data", function(postDataChunk) {
      postData += postDataChunk;
      console.log("Received POST data chunk '"+ postDataChunk + "'.");
    });

    //Complete Post Data - Pass to Handler
    request.addListener("end", function() {
      route(handle, pathname, response, postData);
    }); 
  }
  
  http.createServer(onRequest).listen(8888);
  console.log("BEE has started.");
}

exports.start = start;
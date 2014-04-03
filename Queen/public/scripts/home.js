/*
 * Populate information on the home page from the data received via websockets
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

var socket = io.connect(document.URL + "home");

// Number of connected agents
socket.on('agentcount', function (data) {
  $("#agentcount").html("<h3>Number of Agents : <b>" + data + "</b></h3>")
});

// Timestamp data for every event
socket.on('timestamps', function (data) {
  console.log(data);
  if($.isEmptyObject(data)){
    $('#event-rate').append("<p class=\"alert alert-warning\">No data yet havested - Add Data Sources on the data page!</p>");
  } else {
    sparkline('#event-rate', data);
  }
});

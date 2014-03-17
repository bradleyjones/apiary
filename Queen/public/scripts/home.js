var socket = io.connect(document.URL + "home");

// Number of connected agents
socket.on('agentcount', function (data) {
  $("#agentcount").html("<h3>Number of Agents : <b>" + data + "</b></h3>")
});

// Timestamp data for every event
socket.on('timestamps', function (data) {
  console.log(data);
});

var socket = io.connect(document.URL + "home");

socket.on('agentcount', function(data) {
  $("#agentcount").html("<h3>Number of Agents : <b>" + data + "</b></h3>")
});

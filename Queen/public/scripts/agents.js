var socket = io.connect();

function addAgent(name) {
  $("#agentList").append('<div class="agent"><p>' + name + '</p></div>');
}

function removeAgent(id) {
  var msg = "Agent " + id + " has gone offline";
  addAlert("warning", msg);
}

/*
 * Test Functions
 */
function newAgent() {
  var agentNumber = Math.floor((Math.random()*100)+1);
  socket.emit('newAgent', agentNumber);
  addAgent(agentNumber);
}

function setAgentOffline() {
  var agentNumber = Math.floor((Math.random()*100)+1);
  socket.emit('agentOffline', agentNumber);
  removeAgent(agentNumber);
}

/*
 * Sockets
 */
socket.on('agent', function(data) {
  addAgent(data);
});

socket.on('offline', function(data) {
  removeAgent(data);
});

socket.on('init', function(data) {
  console.log(data.total);
  addAgent(data.total);
});

/*
 * Button Clicks
 */
$(function() {
  $("#new").click(function() {newAgent();});
  $("#remove").click(function() {setAgentOffline();});
});

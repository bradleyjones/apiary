var socket = io.connect();

function addAgent(agent) {
  $("#agent-table").append('<tr id=' + agent.id + '>' +
                           '<th>' + agent.id + '</th>' +
                           '<th>' + agent.machineid +'</th>' +
                           '<th><button class="btn btn-default" ' +
                           'onclick="setAgentOffline(' + agent.id +
                           ')">×</button></th></div>');
}

function removeAgent(id) {
  var msg = "Agent " + id + " has gone offline";
  addAlert("warning", msg);

  //Remove the table row
  var row = document.getElementById(id);
  row.parentNode.removeChild(row);
}

function setAgentOffline(id) {
  socket.emit('agentOffline', id);
  removeAgent(id);
}

/*
 * Test Functions
 */
function newAgent() {
  var agentID = Math.floor((Math.random()*100)+1);
  var agent = {id: agentID, machineid: 01};
  socket.emit('newAgent', agent);
  addAgent(agent);
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
  console.log(data);
  for (var agent in data) {
    addAgent(data[agent]);
  }
});

/*
 * Button Clicks
 */
$(function() {
  $("#new").click(function() {newAgent();});
});

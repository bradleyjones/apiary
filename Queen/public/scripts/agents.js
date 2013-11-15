var socket = io.connect();
var totalAgents = 0;

function addAgent(agent, firstLoad) {
  console.log("AGENT:");
  console.log(agent);
  $("#agent-table").append('<tr id=' + agent.UUID + '>' +
                           '<th><a href=/agents/' + agent.UUID + '>' +
                           agent.UUID + '</a></th>' +
                           '<th>' + agent.machineid +'</th>' +
                           '<th><button class="btn btn-default" ' +
                           'onclick="setAgentOffline(' + agent.UUID +
                           ')">×</button></th></div>');

  totalAgents += 1;
  updateTotal();

  if (!firstLoad) {
    animateIncrease();
  }
}

function removeAgent(id) {
  var msg = "Agent " + id + " has gone offline";
  addAlert("warning", msg);

  //Remove the table row
  var row = document.getElementById(id);
  row.parentNode.removeChild(row);

  totalAgents -= 1;
  updateTotal();

  animateDecrease();
}

function setAgentOffline(id) {
  socket.emit('agentOffline', id);
  removeAgent(id);
}

function updateTotal() {
  $("#total").html(totalAgents + " Agents Connected");
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
  console.log(data);
  var value = null;
  for(var key in data) {
    value = data[key];
  }
  addAgent(value);
});

socket.on('offline', function(data) {
  removeAgent(data);
});

socket.on('init', function(data) {
  console.log(data);
  for (var agent in data.data) {
    console.log(data.data[agent])
    addAgent(data.data[agent], true);
  }
});

/*
 * Button Clicks
 */
$(function() {
  $("#new").click(function() {newAgent();});
});

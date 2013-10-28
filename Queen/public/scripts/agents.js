var socket = io.connect();
var totalAgents = 0;

function addAgent(agent, firstLoad) {
  $("#agent-table").append('<tr id=' + agent.id + '>' +
                           '<th><a href=/agents/' + agent.id + '>' +
                           agent.id + '</a></th>' +
                           '<th>' + agent.machineid +'</th>' +
                           '<th><button class="btn btn-default" ' +
                           'onclick="setAgentOffline(' + agent.id +
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
  addAgent(data.agent);
});

socket.on('offline', function(data) {
  removeAgent(data);
});

socket.on('init', function(data) {
  console.log(data);
  for (var agent in data.agents) {
    data.agents[agent].id = agent
    addAgent(data.agents[agent], true);
  }
});

/*
 * Button Clicks
 */
$(function() {
  $("#new").click(function() {newAgent();});
});

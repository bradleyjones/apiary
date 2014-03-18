var socket = io.connect(document.URL);
var totalAgents = 0;
var agents = [];
var tags;

function addAgent(agent, firstLoad) {
  console.log("AGENT:");
  console.log(agent);

  $('#MyGrid').data().datagrid.options.dataSource._data.push(agent);
  $('#MyGrid').datagrid('reload');

  totalAgents += 1;
  agents.push(agent);
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
 * Sockets
 */
socket.on('agent', function(data) {
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
  for (var agent in data) {
    addAgent(data[agent], true);
  }
});

socket.on('tags', function(data) {
  console.log("TAGSSS");
  console.log(data);
  tags = data;
});

/*
 * Button Clicks
 */
$(function() {
  $("#new").click(function() {
  });
});

function testnewtarget(uuid) {
    console.log("testing new target");
    socket.emit('newTarget', {
      "agents": [uuid],
      "files": ["/test.txt"]
    });
}

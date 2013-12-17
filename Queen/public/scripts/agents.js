var socket = io.connect('http://localhost/agents');
var totalAgents = 0;

function addAgent(agent, firstLoad) {
  console.log("AGENT:");
  console.log(agent);

  $('#MyGrid').data().datagrid.options.dataSource._data.push(agent);
  $('#MyGrid').datagrid('reload');

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

/*
 * Button Clicks
 */
$(function() {
  $("#new").click(function() {
    console.log("testing new target");
    socket.emit('newTarget', {
      "agents": ["fdb34006-3fa8-4641-a5b1-f1c893d029a0"],
      "files": ["/home/bradley/test.txt"]
    });
  });
});

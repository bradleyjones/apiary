var socket = io.connect(document.URL);
var totalAgents = 0;

function addAgent(agent, firstLoad) {
  //console.log("AGENT:");
  //console.log(agent);

  $('#AgentsGrid').data().datagrid.options.dataSource._data.push(agent);
  $('#AgentsGrid').datagrid('reload');

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
  var agents = [];
  for (var agent in data) {
    addAgent(data[agent], true);
    agents.push(data[agent]);
  }
  populateAgentsList(agents);
});

socket.on('tags', function(data) {
  console.log("TAGSSS");
  console.log(data);
  populateTagsList(data);

  for (var t in data) {
    $('#TagsGrid').data().datagrid.options.dataSource._data.push(data[t]);
    $('#TagsGrid').datagrid('reload');
  }

});

/*
 * Button Clicks
 */
$(function() {
  $("#new").click(function() {
  });
});

function newtarget(paths, tags, uuids) {
    var tagsToString = "";
    for (t in tags) {
      tagsToString += tags[t] + ",";
    }
    var sendtags = tagsToString.substring(0, tagsToString.length - 1);
    console.log("testing new target");
    console.log(uuids);
    socket.emit('newTarget', {
      "agents": uuids,
      "files": [{path:paths, tags:sendtags}]
    });
}

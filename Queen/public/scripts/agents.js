var socket = io.connect();

function addAgent(name) {
   $("#agentList").append('<div class="agent"><p>' + name + '</p></div>');
}

function newAgent() {
   var agentNumber = Math.floor((Math.random()*100)+1);
   socket.emit('newAgent', agentNumber);
   addAgent(agentNumber);
}

socket.on('agent', function(data) {
   addAgent(data);
});

$(function() {
   $("#submit").click(function() {newAgent();});
});

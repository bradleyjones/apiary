var socket = io.connect('http://localhost/home');

socket.on('agentcount', function(data) {
  $("#agentcount").html("<h3>Number of Agents : <b>" + data + "</b></h3>")
});

$(function() {
   $("#searchButton").click(function(){
      searchTerm = $("#searchInput")[0].value;
      console.log(searchTerm);
      
      //Edit so data sources and other stuff is also send down with data, Bro
      socket.emit('querySubmit', searchTerm);
   });
});

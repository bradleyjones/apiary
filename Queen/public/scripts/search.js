var socket = io.connect('http://localhost/search');

$(function() {
   $("#searchButton").click(function(){
      searchTerm = $("#searchInput")[0].value;
      console.log(searchTerm);
      
      //Edit so data sources and other stuff is also send down with data, Bro
      socket.emit('querySubmit', searchTerm);
   });
});

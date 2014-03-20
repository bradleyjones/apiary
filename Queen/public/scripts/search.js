var socket = io.connect(document.URL);

$(function() {
   $("#searchButton").click(function(){
      searchTerm = $("#searchTerm")[0].value;
      console.log(searchTerm);

      //Edit so data sources and other stuff is also send down with data, Bro
      socket.emit('querySubmit', searchTerm);
   });
});

$('#results a').click(function (e) {
   e.preventDefault()
   $(this).tab('show')
});

$('#graphs a').click(function (e) {
   e.preventDefault()
   $(this).tab('show')
});

$('#stored a').click(function (e) {
   e.preventDefault()
   $(this).tab('show')
})

//Get Tags
socket.on('tags', function(data){
  console.log("TAGGGSSS");
  console.log(data);
  
  for( var t in data){
    $('#TagList').append(
      "<li><label class='checkbox'>"+data[t][NAME]+"<input type='checkbox' name='' value="+data[t][NAME]+"></input></label></li>"
    )
  }

}

//$('#fieldAccordionButton').click(function (e) {
//  e.preventDefault();
//  $('#fieldAccordion').collapse({
//    toggle: true
//  });
//})


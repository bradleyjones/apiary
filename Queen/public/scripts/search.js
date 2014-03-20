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

//$('#fieldAccordionButton').click(function (e) {
//  e.preventDefault();
//  $('#fieldAccordion').collapse({
//    toggle: true
//  });
//})


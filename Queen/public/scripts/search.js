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
});

//Add Field Button
$('#AddFieldButton').click(function (e) {
   e.preventDefault()
   $('#fieldTabs').append("<li><a href='fieldOne' data-toggle='tab'>A Field</a></li>");
});

//Time Frame Dropdown
function setTimeFrame(timeFrame){
  console.log("Change timeFrame");
  $('#timeFrameDropdown').text(timeFrame + " ").append("<span class='caret'></span>");
  $('#timeFrameDropdown').val(timeFrame);

}

//Add Term ButtonS


/*
 * Sockets
 */
//Get Tags
socket.on('tags', function(data) {
  console.log("TAGGGSSS");
  console.log(data);

  for( var t in data){
    console.log(t);
    $('#TagList').append(
      "<li><label class='checkbox'>"+data[t].NAME+"<input type='checkbox' name='' value="+data[t].NAME+"></input></label></li>"
    )
  }

});

socket.on('results', function(data) {
  console.log('results');
  console.log(data);

  for (var t in data) {
    $('#MyGrid').data().datagrid.options.dataSource._data.push(data[t].log);
    $('#MyGrid').datagrid('reload');
  }
});

//$('#fieldAccordionButton').click(function (e) {
//  e.preventDefault();
//  $('#fieldAccordion').collapse({
//    toggle: true
//  });
//})


var socket = io.connect(document.URL);

$(function() {
   $("#searchButton").click(function(){
      searchTerm = $("#searchTerm")[0].value;
      console.log(searchTerm);
      if(doCheckLuceneQueryValue(searchTerm)){
        //Edit so data sources and other stuff is also send down with data, Bro
        socket.emit('querySubmit', searchTerm);
      }
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
     fieldName = window.prompt("Field Name :", "Field 1");
     $('#fieldTabs').append("<li><a href='"+fieldName+"' data-toggle='tab'>"+fieldName+"</a></li>");
     $('#TermTabs').append("<div id='"+fieldName+"' class='tab-pane fade'></div>");
     //Repopulate Table with field terms and queries
  });
  
  $('#AddTermButton').click(function (e) {
     e.preventDefault()
     console.log("Adding Field Row");
     $("<tr><th>1</th><th><input class='form-control' type='text' value='' placeholder='Bananas'></input></th><th><input class='form-control' type='text' value='' placeholder='Fruit:Banana'></input></th><th><button class='btn btn-default' type='button'>X</button></th></tr>").insertBefore('#termAddButtonRow');
     

     //Add Term to Field
     //Rerun Search?
  });

  $('#addSparkLineButton').click(function (e) {
    //Get search query
    //format data
    //feed to graph
  });

  $('#addPieButton').click(function (e) {
    //Get Search Query
    //Get Field
    //Make Query for each Term in field
    //Parse and format fields and data
    //Feed to graph
    pieChart("#piechart", [{label: "hello", value:10},{label:"2lo",value:5}]);
  });
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

  // reset results
  $('#MyGrid').data().datagrid.options.dataSource._data = [];

  // add data to datagrid
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


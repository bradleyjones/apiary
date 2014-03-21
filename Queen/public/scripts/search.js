var socket = io.connect(document.URL);
var currentSearch = "";

$(function() {
  $("#searchButton").click(function(){
    searchTerm = $("#searchTerm")[0].value;
    console.log(searchTerm);
    if(doCheckLuceneQueryValue(searchTerm)){
      //Edit so data sources and other stuff is also send down with data, Bro
      currentSearch = "";
      socket.emit('querySubmit', searchTerm);
      $('.preloader').show();
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
  $("<tr><th>1</th><th><input class='form-control fieldName' type='text' value='' placeholder='Bananas'></input></th><th><input class='form-control' type='text' value='' placeholder='Fruit:Banana'></input></th><th><button class='btn btn-default' type='button'>X</button></th></tr>").insertBefore('#termAddButtonRow');


  //Add Term to Field
  //Rerun Search?
  });

  // save search
  $('#saveSearch').click( function() {
    console.log("saving search");

    var searchObj = {main:{
      search: currentSearch,
    subsearch: {
    }
    }}

    if (currentSearch != "") {
      socket.emit('saveSearch', currentSearch);
    }
  });

  $('#addSparkLineButton').click(function (e) {
    //Get search query
    //format data
    //feed to graph
  });

  $('#addPieButton').click(function (e) {
    //Get Search Queryi
    searchTerm = $("#searchTerm")[0].value;
    console.log(searchTerm);
    //Get Fields
    fields = $('.fieldName');
    fieldList = []
    console.log(fields);
  fields.each(function(){
    var $field = $(this);
    fieldList.push({
      label : $field.val(),
      subQuery : $field.parent().next().children().val()
    });
  });

  console.log(fieldList);
  //
  //Make Query for each Term in field
  searchParams = {
    main:{
      search: searchTerm,
      subsearch: fieldList
    }
  }

  socket.emit('pieQuerySubmit', searchParams);
  //Parse and format fields and data
  //Feed to graph
  //pieChart("#piechart", [{label: "hello", value:10},{label:"2lo",value:5}]);
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
  $('#SearchGrid').data().datagrid.options.dataSource._data = [];

  // add data to datagrid
  for (var t in data) {
    $('#SearchGrid').data().datagrid.options.dataSource._data.push(data[t].log);
  }

  $('#SearchGrid').datagrid('reload');
  $('.preloader').hide();
});

socket.on('usersSavedSearches', function(data) {
  console.log(data);
});

//HACK CODE, WILL BE STRIPPED OUT
socket.on('pieHackResults', function(data){
  pieChart("#piechart", data);
  // pieChart("#piechart", [{label: "hello", value:10},{label:"2lo",value:5}]);


});

//$('#fieldAccordionButton').click(function (e) {
//  e.preventDefault();
//  $('#fieldAccordion').collapse({
//    toggle: true
//  });
//})


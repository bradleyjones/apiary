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

    addTermToTable();

  //Add Term to Field
  //Rerun Search?
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

$( function() {
$('#SavedGrid').data().datagrid.options.dataSource._data = [];

$('#SavedGrid').data().datagrid.options.dataSource._data.push({NAME:"Demo Query", QUERY:'<a onclick="demoSaved()">Show me all sales</a>'});

$('#SavedGrid').datagrid('reload');

});


  // save search
  function demoSaved() {
    console.log("saving search");

    // TEMP HACK FOR DEMO
    $('#searchTerm').val("CONTENT:SALE");
    addTermToTable('Bananas', 'CONTENT:banana');
    addTermToTable('Apples', 'CONTENT:apple');
    addTermToTable('Pineapples', 'CONTENT:pineapple');
    addTermToTable('Mangos', 'CONTENT:mango');
    addTermToTable('Durians', 'CONTENT:durian');

    //var searchObj = {main:{
      //search: currentSearch,
    //subsearch: {
    //}
    //}}

    //if (currentSearch != "") {
      //socket.emit('saveSearch', currentSearch);
    //}
  }


  function addTermToTable(name, query) {
    var table = document.getElementById('fieldTable');
    var row = table.insertRow(table.rows.length - 1);

    // Insert Count
    //var count = table.rows.length - 2;
    //var count_CELL = row.insertCell(0);
    //count_CELL.innerHTML=count;

    // Insert field name input box
    var fieldName = document.createElement("input");
    fieldName.type = "text";
    fieldName.placeholder = "Bananas";
    fieldName.className = "form-control fieldName";
    if (name != null) {
      fieldName.value = name;
    }
    var fieldName_CELL = row.insertCell(0);
    fieldName_CELL.appendChild(fieldName);

    // Insert sub query input
    var subquery = document.createElement("input");
    subquery.type = "text";
    subquery.placeholder = "CONTENT:banana";
    subquery.className = "form-control"
    if (query != null) {
      subquery.value = query;
    }
    var subquery_CELL = row.insertCell(1);
    subquery_CELL.appendChild(subquery);

    // Add Remove button
    var remove = document.createElement("button");
    remove.className = "btn btn-default";
    remove.type = "button";
    remove.innerHTML = "X";
    remove.onclick = function() {
      var todelete = this.parentNode.parentNode.rowIndex;
      var table = document.getElementById('fieldTable').deleteRow(todelete);
    }
    var remove_CELL = row.insertCell(2);
    remove_CELL.appendChild(remove);
  }



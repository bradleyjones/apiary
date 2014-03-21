var socket = io.connect(document.URL);
var currentSearch = "";

$(function() {
  $("#alertButton").click(function(){
    var query = $('#query-term-search');
    var time = $('#query-term-time');
    var quantity = $('#query-term-quantity');
    var message = $('#query-term-message');

    // VALIDATION
    var error = false;
    if (query.val() == "") {
      query.val("THIS IS A REQUIRED FIELD");
      error = true;
    }
    if (time.val() == "") {
      time.val("THIS IS A REQUIRED FIELD");
      error = true;
    } else if (!isNumeric(time.val())) {
      time.val("THIS SHOULD BE A NUMBER");
      error = true;
    }
    if (quantity.val() == "") {
      quantity.val("THIS IS A REQUIRED FIELD");
      error = true;
    } else if (!isNumeric(quantity.val())) {
      quantity.val("THIS SHOULD BE A NUMBER");
      error = true;
    }
    if (message.val() == "") {
      message.val("THIS IS A REQUIRED FIELD");
      error = true;
    }

    // If no error then submit the alert
    if (!error) {
      var alert = {
        query: query.val(),
        time: Number(time.val()),
        quantity: Number(quantity.val()),
        message: message.val()
      }

      // Set querybar back to nothing
      query.val('');
      time.val('');
      quantity.val('');
      message.val('');

      console.log("submitting alert", alert);

      socket.emit('newalert', alert);
    }
  });
});

function isNumeric(str) {
  return (str==Number(str))?true:false;
}

/*
 * Sockets
 */
socket.on('allalerts', function(data) {
  console.log('All alerts data', data);

  for (var a in data) {
    $('#AlertsGrid').data().datagrid.options.dataSource._data.push(data[a]);
  }

  $('#AlertsGrid').datagrid('reload');
});

socket.on('added', function(data) {
  console.log('New alert has successfully been added', data);

  for ( var first in data ) break;
  data[first].TIMESTAMP = "Just Now";
  $('#AlertsGrid').data().datagrid.options.dataSource._data.push(data[first]);
  $('#AlertsGrid').datagrid('reload');
});

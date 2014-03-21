var socket = io.connect(document.URL);
var currentSearch = "";

$(function() {
  $("#alertButton").click(function(){
    var query = $('#query-term-search').val();
    var time = $('#query-term-time').val();
    var quantity = $('#query-term-quantity').val();
    var message = $('#query-term-message').val();

    // VALIDATION
    var error = false;
    if (query == "") {
      $('#query-term-search').val("THIS IS A REQUIRED FIELD");
      error = true;
    }
    if (time == "") {
      $('#query-term-time').val("THIS IS A REQUIRED FIELD");
      error = true;
    }
    if (!isNumeric(time)) {
      $('#query-term-time').val("THIS SHOULD BE A NUMBER");
      error = true;
    }
    if (quantity == "") {
      $('#query-term-quantity').val("THIS IS A REQUIRED FIELD");
      error = true;
    }
    if (!isNumeric(quantity)) {
      $('#query-term-quantity').val("THIS SHOULD BE A NUMBER");
      error = true;
    }
    if (message == "") {
      $('#query-term-message').val("THIS IS A REQUIRED FIELD");
      error = true;
    }

    // If no error then submit the alert
    if (!error) {
      var alert = {
        query: query,
        time: Number(time),
        quantity: Number(quantity),
        message: message
      }

      console.log("submitting alert", alert);

      socket.emit('newalert', alert);
    }
  });
});

function isNumeric(str) {
  return (str==Number(str))?true:false;
}

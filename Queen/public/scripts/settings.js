$('#btnUpdateSettings').on('click', function() {
  console.log("UPDATING");
  var id = $('#did').val();
  var hrm = $('#dname').val();

  //addDevice(id, hrm);
  post_to_url(document.URL, {id: id, name: hrm});
});

 //id - the id of the device
 //hrm - human readable name
//function addDevice(id, hrm) {
  //device = {id: id, name: hrm};
  //console.log(device);
  //socket.emit('addDevice', device);
//}

//socket.on('addedDevice', function(data) {
  //console.log('added device id');
  //console.log(data);
//});

function post_to_url(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

/*
 * Delete a device
 */
function deleteDevice(uuid) {
  console.log("deleting a device");
  var id = uuid;
  post_to_url(document.URL, {id: id, deleting: true});
}


/*
  Router - Matches requests with handlers
*/

var config = require('./config');

function route(handle, pathname, data) {
  console.log("About to route a request for " + pathname);
  if (typeof handle[pathname] === 'function') {
    handle[pathname](data);
  } else {
    console.log("No request handler found for " + pathname);

    var queueToSendTo = "Error";

    message = {
      action: "ERROR",
      to: "Control",
      from: config.uuid,
      data: "No request handler found for route" + pathname,
      machineid: config.macAddress
    }
          
    connection.publish(queueToSendTo, message,{replyTo: queueName, correlationId: uuid});
    console.log("Sent message: ");
    console.log(message);
} }

exports.route = route;

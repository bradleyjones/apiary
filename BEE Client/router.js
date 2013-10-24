/*
  Router - Matches requests with handlers
*/
function route(handle, pathname, response) {
  console.log("About to route a request for " + pathname);
  if (typeof handle[pathname] === 'function') {
    handle[pathname](response);
  } else {
    console.log("No request handler found for " + pathname);

    var queueToSendTo = "Error";

    message = {
      action: "ERROR",
      to: "Control",
      from: uuid,
      data: "No request handler found for route" + pathname,
      machineid: macAddress
    }
          
    connection.publish(queueToSendTo, message,{replyTo: queueName, correlationId: uuid});
    console.log("Sent message: ");
    console.log(message);
} }

exports.route = route;

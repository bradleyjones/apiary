/*
 * Router - Matches requests with handlers
 *
 * __author__ = "Jack Fletcher"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
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
          
    config.connection.publish(queueToSendTo, message);
    console.log("Sent message: ");
    console.log(message);
} }

exports.route = route;

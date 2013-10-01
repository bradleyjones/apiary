//Request Handlers, Main application logic.
var fs = require('fs');

var hiveIP = 0;

//Initialise - Initialise with Hive IP
function initialise(response, postData) {
  
  hiveIP = postData;
  
  console.log("BEE initialised. Hive IP - "+ hiveIP);
    
  //Add Test Ping
    
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("BEE initialised. Hive IP - "+ hiveIP);
  response.end();
}

//AddTarget - Add a new file to watch
function addTarget(response, postData) {
  
  var file = postData;
  
  console.log("Logging - " + file);
  
  if (hiveIP == 0) {
    throwError("ERROR - Bee not initialised, no Hive address.", response);
  } else if (file == null){
    throwError("ERROR - No Bee target specified.", response);
  } else if (!fs.statSync(file).isFile()){
    throwError("ERROR - Bee target file not found.", response);    
  } else {
    
    startByte = 0;
    
    //Set Starting Byte to the end of the file
    fs.stat(file, function(error, stats){
      if (error) throw error;
      startByte = stats.size;
    });
    
    //Watch File
    fs.watchFile(file, {persistent: true}, function(current, previous){
      console.log(file + " was modified");
      
      //On event, read in new bytes.
      fs.stat(file, function(error, stats){
        if (error) throw error;
        fs.createReadStream(file, {
          encoding: 'ascii',
          start: startByte,
          end: stats.size
        }).addListener("data", function(lines) {
          console.log(lines);
          startByte = stats.size;
        });
      });
    });
  }
}

//RemoveTarget - Remove a target file
function removeTarget(response, postData) {
  console.log("Removing Target");
}

//EXPORT ROUTES
exports.initialise = initialise;
exports.addTarget = addTarget;
exports.removeTarget = removeTarget;

function throwError(message, response){
  console.log(message)
  response.writeHead(500, {"Content-Type": "text/plain"});
  response.write(message);
  response.end();
}
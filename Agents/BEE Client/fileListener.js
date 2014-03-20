/*
  File Watcher
  Watches, and pushes files changes onto MessageBus
*/

//Libraries
var fs = require('fs');
var requestHandler = require('./requestHandlers');

/*
  WatchFile
  Watches a file, calls callback on new lines.
*/
function watchFile(filename, callback){

  var startByte = 0;
    
  //Set Starting Byte to the end of the file
  fs.stat(filename, function(error, stats){
    if (error) throw error;
    startByte = stats.size;
  });
    
  //Watch File
  fs.watchFile(filename, {persistent: true}, function(current, previous){
    console.log(filename + " was modified");
        
    //On event, read in new bytes and pass to callback
    fs.stat(filename, function(error, stats){
      console.log("Comparing old and new");
      if (error) {
        console.log(error);
        throw error;
      }
      var change = fs.createReadStream(filename, {
        start: startByte,
        end: stats.size
      })
      change.on('data', function(data) {
        console.log(data.toString());
        
        stringS = data.toString().split('\n');
        for (string in stringS){
          if(stringS[string]){
            callback(stringS[string]);
          }
        }

        startByte = stats.size;
        change.destroy();
      })
      change.on('error', function(e) {
        console.log(e);
      })
    });
  });
}

//Export Method
exports.watchFile = watchFile;

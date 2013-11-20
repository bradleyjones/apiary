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
      if (error) throw error;
      fs.createReadStream(file, {
        encoding: 'ascii',
        start: startByte,
        end: stats.size
      }).addListener("data", function(){
          callback(lines);
          startByte = stats.size;
      })     
    });
  });
}

//Export Method
exports.watchFile = watchFile;

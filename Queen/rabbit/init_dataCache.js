/*
 * Populate the datacache with all information required in the cache
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

var rabbit = require('./rabbit')
  , dataCache = require('./connection').dataCache;

exports.populate = function() {
  // Get All the Agents
  var msg_getAllAgents = rabbit.constructMessage('ALLAGENTS', 'agentmanager');
  new rabbit.rpc('agentmanager', msg_getAllAgents, function (data) {
    dataCache.agents = data.data;
  });
}

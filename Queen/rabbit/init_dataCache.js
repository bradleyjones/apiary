var rabbit = require('./rabbit')
  , dataCache = require('./connection').dataCache;

exports.populate = function() {
  // Get All the Agents
  var msg_getAllAgents = rabbit.constructMessage('ALLAGENTS', 'agentmanager');
  new rabbit.rpc('agentmanager', msg_getAllAgents, function (data) {
    dataCache.agents = data.data;
  });
}

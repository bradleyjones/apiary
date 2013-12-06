var rabbit = require('./rabbit')
  , dataCache = require('./connection').dataCache
  , main = require('../server.js')
  , io = main.io;

exports.subscribe = function() {
  console.log('calling subscribe function');
  // Look for new agents
  console.log(rabbit)
  new rabbit.pubsub('apiary', 'events.agentmanager.agent.new', function (data) {
    // Update the local data cache with the new data
    for (var k in data) {
      if (data.hasOwnProperty(k)) {
        dataCache.agents[k] = data[k];
      }
    }

    // Send new agents to the agents page
    //io.of('/agents').emit('agent', data);
  });
}

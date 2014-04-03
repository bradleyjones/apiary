/*
 * Setup the initial channels to subscribe to for events
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

var rabbit = require('./rabbit')
  , dataCache = require('./connection').dataCache
  , main = require('../server.js')
  , io = main.io;

exports.subscribe = function() {
  console.log('calling subscribe function');
  // Look for new agents
  console.log(rabbit)
  new rabbit.pubsub('apiary', 'events.agentmanager.agent.new', function (msg) {
    // Update the local data cache with the new data
    for (var k in msg.data.agents) {
      if (msg.data.agents.hasOwnProperty(k)) {
        dataCache.agents[k] = msg.data.agents[k];
      }
    }

    // Send new agents to the agents page
    io.of('/agents').emit('agent', msg.data.agents);
    // Send new agents to the home page
    io.of('/home').emit('agent', msg.data.agents);
  });
}

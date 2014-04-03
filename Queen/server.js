/*
 * Initial Setup of the Queen server
 *
 * Handles:
 *  - configuring express and all other required libraries
 *  - setup authentication and logic for users logging in and out
 *  - routes to other controllers
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

"use strict";

// Setup all the required libraries
var http = require('http')
  , express = require('express')
  , app = express()
  , server = http.createServer(app)
  , io = require('socket.io')
  , MongoStore = require('connect-mongo')(express)
  , colors = require('colors')
  , config = require('./config/config')
  , connect = require('express/node_modules/connect')
  , cookie = require('cookie');


var session_store = new connect.middleware.session.MemoryStore;
exports.session_store = session_store;

// Setup express to use views and public folder
// Use Jade as the template engine for views
app.configure(function () {
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.set("view options", { layout: false });
  app.use(express.json());
  app.use(express.urlencoded());
  app.use(express.methodOverride());
  // Use mongodb to store sessions
  app.use(express.cookieParser());
  app.use(express.session({
    secret: 'THISISASECRETSSHHH',
    key: 'express.sid',
    store: session_store
  }));
  app.use(app.router);
  app.use(express.static(__dirname + '/public'));
});

// Populate the DataCache by making all the initial
// RPC calls to the Hive
var connection = require('./rabbit/connection')._conn;
connection.on('ready', function() {
  console.log("connected to ".green + connection.serverProperties.product.green);
  var initData = require('./rabbit/init_dataCache');
  initData.populate();
  var initSubscribes = require('./rabbit/init_subscribes');
  initSubscribes.subscribe();
})
connection.on('error', function(e) {
  throw e;
});

// Start listening
server.listen(3000, function(){
  console.log("Queen is listening on port %d".green, server.address().port)
})

// Setup socket IO
exports.io = io.listen(server).set('authorization', function(data, accept) {
  console.log(data);
  if (!data.headers.cookie) {
    return accept('No cookie transmitted.', false);
  }

  data.cookie = cookie.parse(data.headers.cookie);

  console.log("cookie        ",data.cookie['express.sid'])
  data.sessionID = data.cookie['express.sid'].substring(2,26);

  session_store.load(data.sessionID, function(err, session) {
    console.log(session)

    if (err || !session) return accept('Error', false);

    data.session = session;
    return accept(null, true);
  });
});

/*
 *  Authentication
 */

var mongoose = require('mongoose')
  , User = require('./models/user')
  , Device = require('./models/device');

// Connect to MongoDB
mongoose.connect('mongodb://' + config.mongoIP + ':27017/queen-users', function(err){
  if (err) {
    console.log("Unable to connect to mongodb".red);
    console.log("Start the mongodb daemon by running \"mongod\"".red);
    throw err;
  };
  console.log('Connected to MongoDB'.green);
});

// Function to check there is a user logged in
function checkAuth(req, res, next) {
  if (!req.session.user_id) {
    // Check that there is at least one user in the database
    User.count({}, function(err, count){
      if (err) throw err;
      if (count > 0) {
        res.render('login.jade');
      } else {
        res.render('newuser.jade');
      }
    });
  } else {
    // Stop caching of restricted pages
    res.header('Cache-Control', 'no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0');
    next();
  }
}

// logic to control what happens when a user tries to login and authenticate
app.post('/login', function (req, res) {
  console.log(req);
  var post = req.body;
  // Find a user with matching username
  User.findOne({ username: post.user }, function(err, user){
    if (!user) {
      res.redirect('/');
    } else {
      // If a user is found check the password is correct
      user.comparePassword(post.password, function(err, isMatch){
        if (err) throw err;
        req.session.user_id = user._id;
        // If the request contains a device_id, create a new device (if it is new)
        var devid = post.device_id;
        var devname = post.device_name;
        if (devid != null) {
          if (devname == null) {
            devname = "Device";
          }
          var newDevice = new Device({
            device_id: devid,
            device_name: devname
          });
          newDevice.save(function(err) {
            if (err) {
              // Do Nothing
            } else {
              User.update({ _id: user._id },
              {$push : {
                // Push the id of the new device in the DB
                devices : newDevice._id
                  }},
              function(err, model) {
                if (err) {
                  throw err;
                  console.log("there was an error adding device");
                }
              });
            }
          });
        }
        res.redirect('/');
      });
    }
  });
});

// Log the current user out
app.get('/logout', function (req, res) {
  delete req.session.user_id;
  res.redirect('/');
});

// Render the page to create a new user
app.get('/newuser', function(req, res) {
  delete req.session.user_id;
  res.render('newuser.jade');
});
// Create a new user
app.post('/newuser', function (req, res) {
  var post = req.body;

  // Validation
  if(!post.user || !post.password){
    res.render('newuser.jade');
  } else {
    var newuser = new User({
      username: post.user,
      password: post.password
    });
    newuser.save(function(err){
      if (err) throw err;
      req.session.user_id = newuser._id;
      res.redirect('/');
    });
  }
});


/*
 *  Routes
 */

// Render the home page
var home = require('./controllers/home');
app.get('/', checkAuth, home.index);

// Render the search page
var search = require('./controllers/search');
app.get('/search', checkAuth, search.index);

// Render the alerts page
var alerts = require('./controllers/alerts');
app.get('/alerts', checkAuth, alerts.index);

// Render the agents/data page
var agents = require('./controllers/agents');
app.get('/agents', checkAuth, agents.list);
app.get('/agents/:id', checkAuth, agents.individual);

// Render the settings page
var settings = require('./controllers/settings');
app.post('/settings', checkAuth, settings.update);
app.get('/settings', checkAuth, settings.index);

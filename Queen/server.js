"use strict";

// Setup all the required libraries
var http = require('http')
  , express = require('express')
  , app = express()
  , server = http.createServer(app)
  , io = require('socket.io').listen(server)
  , MongoStore = require('connect-mongo')(express)
  , colors = require('colors');

exports.io = io;

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
    store: new MongoStore({
      db: 'queensessions'
    })
  }));
  app.use(app.router);
  app.use(express.static(__dirname + '/public'));
});

// Start listening
server.listen(3000, function(){
  console.log("Queen is listening on port %d".green, server.address().port)
})

/*
 *  Authentication
 */

var mongoose = require('mongoose')
  , User = require('./models/user');

mongoose.connect('mongodb://localhost:27017/queen-users', function(err){
  if (err) {
    console.log("Unable to connect to mongodb".red);
    console.log("Start the mongodb daemon by running \"mongod\"".red);
    throw err;
  };
  console.log('Connected to MongoDB'.green);
});

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

app.post('/login', function (req, res) {
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
        res.redirect('/');
      })
    }
  });
});

app.get('/logout', function (req, res) {
  delete req.session.user_id;
  res.redirect('/');
});

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
var home = require('./controllers/home')
app.get('/', checkAuth, home.index);

var agents = require('./controllers/agents');
app.get('/agents', agents.list);
app.get('/agents/:id', agents.individual);

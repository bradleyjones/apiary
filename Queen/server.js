"use strict";

// Setup all the required libraries
var http = require('http')
  , express = require('express')
  , app = express()
  , server = http.createServer(app)
  , io = require('socket.io').listen(server)
  , MongoStore = require('connect-mongo')(express)
  , mongoose = require('mongoose')
  , User = require('./models/user');

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
  console.log("Queen is listening on port %d", server.address().port)
})

/*
 *  Authentication
 */

function checkAuth(req, res, next) {
  if (!req.session.user_id) {
    res.render('login.jade');
  } else {
    // Stop caching of restricted pages
    res.header('Cache-Control', 'no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0');
    next();
  }
}

app.post('/login', function (req, res) {
  var post = req.body;
  console.log(post);
  if (post.user == 'user' && post.password == 'pass') {
    req.session.user_id = 1;
    res.redirect('/');
  } else {
    res.send('Bad user/pass');
  }
});

app.get('/logout', function (req, res) {
  delete req.session.user_id;
  res.redirect('/');
});


/*
 *  Routes
 */

// Render the home page
app.get('/', checkAuth, function (req, res) {
    res.render('home.jade');
});

var agents = require('./controllers/agents');

app.get('/agents', agents.list);
app.get('/agents/:id', agents.individual);



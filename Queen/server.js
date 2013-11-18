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
  app.use(express.methodOverride());
  // Use mongodb to store sessions
  app.use(express.cookieParser());
  app.use(express.session({
    secret: 'THISISASECRETSSHHH',
    store: new MongoStore({
      db: 'queensessions'
    })
  }));
  app.use(express.static(__dirname + '/public'));
});

// Render the home page
app.get('/', function (req, res) {
    res.render('home.jade');
});

// Start listening
server.listen(3000, function(){
  console.log("Queen is listening on port %d", server.address().port)
})

/*
  Routes
*/
var agents = require('./controllers/agents');

app.get('/agents', agents.list);
app.get('/agents/:id', agents.individual);



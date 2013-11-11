"use strict";

// Setup all the required libraries
var http = require('http');
var express = require('express');
var app = express();
var server = http.createServer(app).listen(3000);
var jade = require('jade');
var io = require('socket.io').listen(server);

// Setup express to use views and public folder
// Use Jade as the template engine for views
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.set("view options", { layout: false });
app.configure(function () {
    app.use(express.static(__dirname + '/public'));
});

// Render the home page
app.get('/', function (req, res) {
    res.render('home.jade');
});

/*
  Routes
*/
var agents = require('./controllers/agents');

app.get('/agents', agents.list);
app.get('/agents/:id', agents.individual);

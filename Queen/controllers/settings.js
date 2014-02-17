"use strict";

var main = require('../server.js')
  , io = main.io;
var mongoose = require('mongoose')
  , User = require('../models/user');

exports.update = function(req, res) {
  var userid = req.session.user_id;
  console.log(userid);

  console.log(req.body);

  var devid = req.body.id;
  var devname = req.body.name;

  console.log(devid + devname);
  User.update({ _id: userid },
      {device_id: devid, device_name: devname},
      function(err, model) {
        if (err) {
          console.log("there was an error adding device");
        } else {
          res.redirect('/settings');
        }
      });

  // Web Sockets
  //io.on('connection', function(socket) {
    //socket.on('addDevice', function(data) {
      //console.log(data);
      //console.log(userid);
      //User.findOne({ id: \ci})
    //});
  //});
};

exports.index = function(req, res) {
  var user = User.findOne({ _id: req.session.user_id }, function(err, user) {
    console.log(user);
    res.render("settings.jade", { id: JSON.stringify(user.device_id), name: JSON.stringify(user.device_name)});
  });
};

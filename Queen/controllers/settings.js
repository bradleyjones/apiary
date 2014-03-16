"use strict";

var main = require('../server.js')
  , io = main.io
  , mongoose = require('mongoose')
  , User = require('../models/user')
  , Device = require('../models/device');

exports.update = function(req, res) {
  var userid = req.session.user_id;
  console.log(userid);

  console.log(req.body);

  var devid = req.body.id;
  var devname = req.body.name;

  // Create a new device in the DB
  var newDevice = new Device({
    device_name: devname,
    device_id: devid
  })
  newDevice.save(function(err) {
    if (err) throw err;
  });

  console.log(devid + devname);
  User.update({ _id: userid },
      {$push : {
            // push the id of the new device in the DB
            devices : newDevice._id
              }},
      function(err, model) {
        if (err) {
          throw err;
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

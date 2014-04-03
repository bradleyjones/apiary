/*
 * Settings controller, controls loading the page as well as routes which allow
 * the user to update/add new devices to the user model
 *
 * TODO - Change from using routes to control updates/new devices to using
 * websockets to be in line with the rest of Queen
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

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

  if (req.body.deleting != null) {
    // delete an existing device

    var uuid = req.body.id;
    var devid;

    // remove the device from the device table
    Device.findOne({ device_id: uuid}, function (err, dev) {
      if (err) throw err;

      devid = dev._id;

      dev.remove();

      console.log("Device to be deleted");
      console.log(dev);
    });

    //remove the device from the user table
    User.findOne({ _id: userid}, function (err, user) {
        if (err) {
          console.log("there was an error removing device");
        } else {
          user.devices.remove(devid);
          console.log("User to delete device from");
          console.log(user);
          res.redirect('/settings');
        }
    });

  } else {
    // Add a new device

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
  }
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

    var devices = [];
    var deleted = 0;
    for (var i = 0; i < user.devices.length; i++) {
      var dev = user.devices[i];
      console.log(dev);
      Device.findOne({ _id: dev }, function(err, tmp) {
        if (tmp != null) {
          console.log(tmp);
          devices.push( { UUID: tmp.device_id, NAME: tmp.device_name} );
        } else {
          deleted++;
        }
        console.log(i);
        console.log(user.devices.length);
        // if at the last device render the page
        if (devices.length == (user.devices.length-deleted)) {
          console.log("SENDING DEVICES");
          console.log(devices);
          res.render("settings.jade", { devices : JSON.stringify(devices) });
        }
      });
    }

    if (user.devices.length == 0) {
      res.render("settings.jade");
    }
  });
};

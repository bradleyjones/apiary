/*
 * Model for a Device
 */

var mongoose = require("mongoose")
  , Schema = mongoose.Schema;

var DeviceSchema = new Schema({
  device_name: { type: String, required: true},
  device_id: { type: String, required: true, index: {unique: true}}
});

module.exports = mongoose.model('Device', DeviceSchema);

/*
 * Mongo model for a Device
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

var mongoose = require("mongoose")
  , Schema = mongoose.Schema;

var DeviceSchema = new Schema({
  device_name: { type: String, required: true},
  device_id: { type: String, required: true, index: {unique: true}}
});

module.exports = mongoose.model('Device', DeviceSchema);

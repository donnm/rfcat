var util = require('util');

var bleno = require('bleno');

var BlenoCharacteristic = bleno.Characteristic;

var PythonShell = require('python-shell');
var EdisonCtl = new PythonShell('../ExplorerCtl.py');

EdisonCtl.on('message', function(message) {
  console.log(message);
  // got a message from EdisonCtl.py, so send it to notificatons
 
  if (SerialChara._updateValueCallback != null) {
    Serial.Chara._updateValueCallback(message);
  } 
});

function SerialChara() {
  SerialChara.super_.call(this, {
    uuid: '8a53fa01d9d242afb942ce50a39bc7e6',
    properties: ['read', 'write', 'notify'],
    value: null
  });

  this._value = new Buffer(0);
  this._updateValueCallback = null;
};

util.inherits(SerialChara, BlenoCharacteristic);

SerialChara.prototype.onReadRequest = function(offset, callback) 
{
  console.log('SerialChara - onReadRequest: value = ' + 
this._value.toString('hex'));

  callback(this.RESULT_SUCCESS, this._value);
};

SerialChara.prototype.onWriteRequest = function(data, offset, 
withoutResponse, callback) {
  this._value = data;

  console.log('SerialChara - onWriteRequest: value = ' + 
this._value.toString('hex'));

  cmd = '';
  for (var i = 0; i < data.length; i++) {
    cmd += data[i].toString() + ',';
  }
  cmd = cmd.substring(0, cmd.length - 1); 
  // write to pyserial script
  console.log('sending: ' + cmd);
  EdisonCtl.send(cmd); 
  callback(this.RESULT_SUCCESS);
};

SerialChara.prototype.onSubscribe = function(maxValueSize, 
updateValueCallback) {
  console.log('SerialChara - onSubscribe');

  this._updateValueCallback = updateValueCallback;

};

SerialChara.prototype.onUnsubscribe = function() {
  console.log('SerialChara - onUnsubscribe');

  this._updateValueCallback = null;

};

module.exports = SerialChara;

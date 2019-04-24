var bleno = require('bleno');

var BlenoPrimaryService = bleno.PrimaryService;

var wi_serial = require('./serial-chara');

var SerialChara = new wi_serial();

console.log('bleno - WiSerial');

bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);

  if (state === 'poweredOn') {
    bleno.startAdvertising('WiSerial', 
['8a53fa01d9d242afb942ce50a39bc7e0']);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 
'success'));

  if (!error) {
    bleno.setServices([
      new BlenoPrimaryService({
        uuid: '8a53fa01d9d242afb942ce50a39bc7e0',
        characteristics: [
          SerialChara
        ]
      })
    ]);
  }
});

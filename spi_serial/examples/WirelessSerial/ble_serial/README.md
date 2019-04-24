
This node.js project serves as a BLE endpoint to test a BLE->Explorer block communications link.

# Dependencies

You'll need to install bleno and python-shell

~~~~
npm install bleno
npm install python-shell
~~~~

# Setting Up and Running
You have to set up Bluetooth on the Edison properly before you can successfully run this example. On the 3.5 version of Edison Yocto, you can do this as follows:

~~~~
ps | grep bluetoothd
~~~~

Identify the process ID number of bluetoothd, then do the following

~~~~
kill bluetoothd_id_num
rfkill unblock bluetooth
hciconfig hci0 up
~~~~

Then run the BLE endpoint as follows:

~~~~
node main.js
~~~~

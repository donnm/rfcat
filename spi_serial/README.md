
Intel Edison Software Library for 915MHz Explorer Block

This software is released under the MIT license. See the accompanying
LICENSE.txt for more details.

# Pre-Requisites

The Explorer board libraries require a current version of MRAA to run. MRAA allows the Explorer software to control the Edison's input/output pins directly.

If you're running yocto, do the following:

    echo "src mraa-upm http://iotdk.intel.com/repos/3.0/intelgalactic/opkg/i586" > /etc/opkg/mraa-upm.conf
    opkg update
    opkg install mraa

If you're running ubilinux/jubilinux, follow the instructions here:
https://learn.sparkfun.com/tutorials/installing-libmraa-on-ubilinux-for-edison

### mraa with support for non-root users

Currently, mraa only works with root access. There's a branch of mraa that gets around this for the Edison, and if you want non-root users to be able to use mraa you can try the following (courtesy of brendan.le.foll@intel.com).

> It’s in this branch https://github.com/intel-iot-devkit/mraa/tree/edison-perms. Imraa can be run with this config file: https://github.com/intel-iot-devkit/mraa/blob/edison-perms/imraa/imraa.io.edison.conf. Switch out ‘brendan’ for user/group combo of your choice and you can set gpio/i2c/spi to a user of your choice. Note that the first 4 lines are what you can edit, the rest should be left as is (we can only support ‘one’ user although you can play with groups to do combinations etc…). You will also need to chmod +x /sys/kernel/debug.
> 
> I’ve given it a quick run through and gpio/i2c/spi seems to work on my Arduino breakout, should work on others but may need a bit of tweaking in the config, syslog should tell you and you can add the IO as a raw pin, uart/pwm/aio needs a bit more work but should be easy to add. It’s a bit too Edison specific to get merged right now but with a bit more tweaking I think I can improve it a lot.
> 
> To run imraa:
> $ imraa –I imraa.io.edison.conf
> 
> You can run it with the systemd service file provided and put the config in /etc/imraa.conf. That way you don’t need the –I flag.

# Setup


On your Intel Edison, run the following after connecting it to the internet:

    mkdir ~/src
    cd ~/src
    git clone https://github.com/EnhancedRadioDevices/spi_serial.git
    cd spi_serial
    python setup.py install

# CC1110 Firmware

This software library is intended to work with a specific firmware variant on
the TI CC1110.

You can get that firmware from:
https://github.com/EnhancedRadioDevices/subg_rfspy

## Installing new firmware onto the CC1110

While the default firmware for the CC1110 should work well with this library,
there are cases where you'd want to change or update. To do that, please use
the ccprog library from @ps2.

https://github.com/ps2/ccprog

Once you've cloned and made that program, you can flash a new hex file to the CC1110 using the following commands:

    wget https://github.com/EnhancedRadioDevices/subg_rfspy/releases/download/v0.8-explorer/spi1_alt2_EDISON_EXPLORER_US_STDLOC.hex
    ccprog -p 19,7,36 erase
    ccprog -p 19,7,36 write spi1_alt2_EDISON_EXPLORER_US_STDLOC.hex

Note: the 19,7,36 numbers in the above string refer to the Edison hardware
pins that are used to communicate with the CC1110. If you aren't using the
Explorer board, you may need to use different pin numbers.

# Testing

Once you have the Explorer software and firmware loaded, you should be able to run the Explorer hardware test script to verify that everything is working. Unit tests can be run as follows:

    cd ~/src/spi_serial/tests
    python unit_test.py
	
The unit test checks to make sure the different commands function properly. After testing each function it will state whether it was a success or failure. At the end of the test it will print a summary and indicate if any of the commands failed.
This test script can take some optional arguments.

## Channel Selection (-c)

Select which channel to test the transmit/receive functions on. If not specified, this option defaults to '0'. For example:

    python unit_test.py -c 13

## Transmit/Receive Order ([-t|-r])

This option is for if you have two Explorers and want to test their transmit/receive functionality. If not specified, the test will skip testing transmit/receive functionality.

Start the test script for the receiving Explorer first. For example:

	python unit_test -r

Then, on the other Explorer:

	python unit_test -t
	
## Transceive Cycles (-s)

This option sets the number of transmit/receive cycles to test, if a transmit/receive order has also been selected. This option defaults to '10' if not specified. For example:

	python unit_test -r -s 42

This will run through 42 transmit/receive cycles. If a different value is chosen for each Explorer, then the test will not complete successfully.


# Examples

There are also some examples that you can look at to see how to use the library. The best place to start is probably:

    cd ~/src/spi_serial/examples
    python ExplorerTest.py
    
This should return an OK message and blink the two user LEDs on the Explorer board. If that happens, your board is working well.

There's also a set of examples showing how to use the Edison/Explorer system as a BLE to 915MHz bridge. You can find those in spi_serial/examples/WirelessSerial

If you have two Explorers and would like to perform a more thorough test you can perform the following steps:
1. Plug battery into Explorer. The PWR LED should light up.
2. Connect USB into the UART port. The PWR LED should stay lit and the CHRG LED should light up (battery should be allowed to partially discharge beforehad to test CHRG)
3. Run the following commands:

	cd ~/src/spi_serial/examples/Wireless
	python RemoteLEDs.py
	
This should return a message about finding the CC1110 and indicate that it is waiting for a packet.
4. From the second Explorer run the following commands:

	cd ~/src/915MHzEdisonExplorer_SW/Examples/Wireless
	python ExplorerCtl.py
	4,0,0,0,8,1,1,0
	
The first Explorer should print the received packet preceeded by RSSI and packet number e.g. [82,1,8,1,1,0]. The LED labeled D2 should also light up.
5. Switch the USB on the first Explorer from the UART to the OTG. The PWR and D2 LEDs should remain lit. On your computer you should see a volume labled "Edison" become available.
6. Remove the battery. The PWR and D2 LEDs should remain lit. The volume "Edison" should remain available.

If every step gave the described results then your board is working well.

If you have a USB On-The-Go cable or adaptor, you can quickly test the OTG port functionality. 
1. Connect to your Explorer Board as normal (using the USB UART port) and log in.
2. Using the USB OTG cable, connect any Android device (such as a phone) to the USB OTG port on the Explorer.
3. Run the following command:

	lsusb

If your response looks like this: 

	unable to initialize libusb: -99

Try flipping your OTG cable around.

If it working correctly, you should see an output that looks something like this: 

	Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
	Bus 001 Device 004: ID 04e8:686c Samsung Electronics Co., Ltd
	Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	
If you see this, then your USB OTG port is working well.

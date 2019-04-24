
# 915MHz Serial Link

The python script in this directory allows for simple tranmission of commands and data to the CC1110. The CC1110 can parse these commands and then transmit and receive data with other Explorer boards as needed.

# BLE to Serial Link

This example serves as a BLE to 915 serial bridge. Running the node.js script will start a BLE peripheral with one characteristic. Writing to that characteristic (from e.g. a Smartphone) will cause the string you write to be transmitted to the CC1110 on the Explorer board and interpreted as a serial command.

# ExplorerCtl.py

## Command structure

cmd_id,cmd_payload

## Resetting the CC1110

7

## Changing LEDs

8,led_num,on_noff

## Sending a packet

4,channel,repeat_cnt,delay_ms,payload

### Payload Structure

payload must end with 0

ex: 4,8,0,0,1,2,3,4,5,6,7,8,0

## Receiving a Packet

3,channel,timeout0,timeout1,timeout2,timeout3

ex: 3,8,0,1,2,3
py-ble-hci
==========

A binary parser for Bluetooth 4.0 HCI packets along with a TCP controlled serial port server allowing a remote, interactive and scriptable HCI session.

Serial commands are built from Python objects and responses are parsed into objects for easy programmatic access. Controller responses are parsed and their success status is checked before each command returns.

Example image shows two servers controlled by one client.

Made in order to control DTM sessions, but easily expandable to other HCI commands/events. Parser built from [construct](http://construct.wikispaces.com/) package, serial from [pyserial](http://pyserial.sourceforge.net/). __Both required to run__. I used construct 2.06 and pyserial 2.6 on python 2.7.3.

Built with a focus on the [Texas Instruments CC2540](http://processors.wiki.ti.com/index.php/Category:BluetoothLE) USB dongle, with the 'host_test_release' firmware which emulates a serial port when connected to a PC.

Demo
----
![demonstration run](https://raw.githubusercontent.com/hughobrien/py-ble-hci/master/demo_run.png)

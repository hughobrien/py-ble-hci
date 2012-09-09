from time import sleep
from scripting import *
from structs import parse, build
import comms
import threading

#transmitter = "/dev/ttyACM0"
transmitter_path = "\\.\COM6"
receiver_path = "\\.\COM7"

transmitter = comms.setup_serial_port(transmitter_path, debug_level=0)
threading.Thread(target=comms.reader, args=(transmitter,)).start()

receiver = comms.setup_serial_port(receiver_path, debug_level=0)
threading.Thread(target=comms.reader, args=(receiver,)).start()

do_rx(receiver,channel=23)
do_tx(transmitter,channel=23, payload_len=20, pattern='z1111')

sleep(5)

do_test_end(transmitter)
print do_test_end(receiver) #received packet count

transmitter.close()
receiver.close()

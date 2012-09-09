from time import sleep
from scripting import *
from structs import parse, build
import comms
import threading

#transmitter = "/dev/ttyACM0"
transmitter_path = "\\.\COM6"
receiver_path = "\\.\COM7"

transmitter = comms.setup_serial_port(transmitter_path)
transmitter.close() #sanity
transmitter.open()
threading.Thread(target=comms.reader, args=(transmitter,)).start()

receiver = comms.setup_serial_port(receiver_path)
receiver.close()
receiver.open()
threading.Thread(target=comms.reader, args=(receiver,)).start()


do_rx(receiver,channel=23)
response = parse(receiver.last_rx)
if response.event_opcode == 'cmd_complete':
    if response.event_params.cmd_response.status == 'success':
        print "\nListening...\n"
        
do_tx(transmitter,channel=23, payload_len=20, pattern='z1111')
response = parse(transmitter.last_rx)
if response.event_opcode == 'cmd_complete':
    if response.event_params.cmd_response.status == 'success':
        print "\nTransmitting..."

sleep(5)
print

do_test_end(transmitter)
response = parse(transmitter.last_rx)
if response.event_opcode == 'cmd_complete':
    if response.event_params.cmd_response.status == 'success':
        print "\nTransmission Ended\n"

do_test_end(receiver)
response = parse(receiver.last_rx)
if response.event_opcode == 'cmd_complete':
    if response.event_params.cmd_response.status == 'success':
        print "\nPacket Count: %d\n" % response.event_params.cmd_response.pkt_count

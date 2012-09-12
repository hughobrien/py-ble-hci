import comms
from time import sleep
from scripting import *
from utils import *

tx_host = "10.0.0.2"
tx_port = 2347
rx_host = "10.0.0.2"
rx_port = 2348

transmitter = comms.open_socket(tx_host, tx_port)
receiver = comms.open_socket(rx_host, rx_port)

do_cmd(transmitter, 'le_reset')
do_cmd(receiver, 'le_reset')
sleep(2)

packet_counters = []
for length in [0, 15, 30]:
    do_rx(receiver, channel=37)
    do_tx(transmitter, channel=37, pattern='z1111', payload_len=length)

    sleep(3)

    do_test_end(transmitter)
    packet_counters.append(do_test_end(receiver))

transmitter.close()
receiver.close()

print packet_counters

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


pattern = 'psn9'
length = 10

results = {}

for channel in range(0,40):
    counts = []
    for i in range(0,9):
        do_rx(receiver, channel=channel)
        do_tx(transmitter, channel=channel, payload_len=length, pattern=pattern)
        sleep(5)
        do_test_end(transmitter)
        counts.append(do_test_end(receiver))

    results[channel] = counts

transmitter.close()
receiver.close()

dict_to_csv(results, 'data.csv')
print results

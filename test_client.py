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

results = {}

for length in [0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 37]:
    counts = []
    for i in range(0,10):
        do_rx(receiver)
        do_tx(transmitter, payload_len=length)
        sleep(5)
        do_test_end(transmitter)
        counts.append(do_test_end(receiver))
        
    results[length] = counts

transmitter.close()
receiver.close()

dict_to_csv(results, 'data.csv')
print results

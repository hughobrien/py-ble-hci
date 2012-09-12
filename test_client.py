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

results = {}

for length in [30, 20, 10, 0]:
    counts = []
    for i in range(0,10):
        do_rx(receiver)
        do_tx(transmitter, payload_len=length)
        
        sleep(10)
        
        do_test_end(transmitter)
        counts.append(do_test_end(receiver))

        do_cmd(transmitter, 'le_reset')
        do_cmd(receiver, 'le_reset')
        
    results[length] = counts


transmitter.close()
receiver.close()

dict_to_csv(results, 'data.csv')
print results

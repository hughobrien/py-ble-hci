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

time_range = [5, 10, 20]
length_range = [0, 15, 30]
channel_range = [10, 25, 39]
pattern_range = ['psn9', 'z1111', 'z1010']
num_runs = 10

pps = []

for time in time_range:
    for channel in channel_range:
        for length in length_range:
            for pattern in pattern_range:
                for i in range(num_runs):
                    
                    do_rx(receiver, channel=channel)
                    do_tx(transmitter, channel=channel, payload_len=length, pattern=pattern)

                    sleep(time)
            
                    do_test_end(transmitter)
                    count = do_test_end(receiver)

                    do_cmd(transmitter, 'le_reset')
                    do_cmd(receiver, 'le_reset')

                    print "%ds on ch%d length %d ptrn %s run%d yielded %d packets" % (time, channel, length, pattern, i, count)
                    rate = float(count) / float(time)
                    pps.append(rate)
                    print "%g packets per second" % rate


transmitter.close()
receiver.close()

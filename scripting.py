from construct import *
from utils import *
from structs import build, parse
from time import sleep

def tx_container(channel=0, payload_len=10, test_pattern='psn9'):
        container = Container(
                pkt_type = 'command',
                cmd_opcode = 'tx_test',
                cmd_params = Container(
                        channel = channel,
                        payload_len = payload_len,
                        test_pattern = test_pattern,
                        ),
                )
        container.param_len = len(container.cmd_params)
        return container

def rx_container(channel=0):
        container = Container(
                pkt_type = 'command',
                cmd_opcode = 'rx_test',
                cmd_params = Container(
                        channel = channel
                        ),
                )
        container.param_len = len(container.cmd_params)
        return container

def cmd_container(opcode, cmd_params=[]):
        return Container(
                pkt_type = 'command',
                cmd_opcode = opcode,
                param_len = len(cmd_params),
                cmd_params = cmd_params,
                )
                
                
def write(data,port,block=False):
        port.last_tx = data
        print "Sent: %s" % pretty(data)
        port.write(data)

        if block == True:
                port.rxing = True
                while port.rxing == True:
                        sleep(0.1)
        
        
def hand_code(input,port):
        write(pack(input), port)

def do_cmd(port, opcode, data=[]):
        container = cmd_container(opcode, data)
        raw = build(container)
        print container
        write(raw, port,block=True)
        
def do_tx(port,channel=0, payload_len=10, pattern='psn9'):
        container = tx_container(channel,payload_len,pattern)
        raw = build(container)
        print container
        write(raw,port,block=True)
        
        
def do_rx(port,channel=0):
        container = rx_container(channel)
        raw = build(container)
        print container
        write(raw,port,block=True)
        
def do_test_end(port):
        container = cmd_container('test_end')
        raw = build(container)
        print container
        write(raw,port,block=True)

def do_reset(port):
        do_cmd(port, 'util_reset')

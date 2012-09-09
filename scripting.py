from construct import *
from utils import *
from structs import build, parse

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
                
                
def write(data,port):
        port.last_tx = data
        print "Sent: %s" % pretty(data)
        port.write(data)
        
def hand_code(input,port):
        write(pack(input), port)

def do_cmd(port, opcode, data=[]):
        container = cmd_container(opcode, data)
        raw = build(container)
        write(raw, port)
        print container
        
def do_tx(port,channel=0, payload_len=10, pattern='psn9'):
        container = tx_container(channel,payload_len,pattern)
        raw = build(container)
        write(raw,port)
        print container
        
        
def do_rx(port,channel=0):
        container = rx_container(channel)
        raw = build(container)
        write(raw,port)
        print container
        
def do_test_end(port):
        container = cmd_container('test_end')
        raw = build(container)
        write(raw,port)
        print container

def do_reset(port):
        do_cmd(port, 'util_reset')


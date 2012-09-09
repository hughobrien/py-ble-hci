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
        if port.debug_level > 0:
                print "Sent: %s" % pretty(data)
        port.write(data)

        if block:
                port.rxing = True
                while port.rxing == True:
                        sleep(0.1)
        
        
def hand_code(input,port):
        write(pack(input), port)

def check_response(port):
        response = parse(port.last_rx)
        if response.event_opcode == 'cmd_complete':
                if response.event_params.cmd_response.status == 'success':
                        if port.debug_level > 0:
                                print "Success"
                        return
        print "Fault:\n%s" % repr(response)

def build_write_check(port,container):
        raw = build(container)
        if port.debug_level == 2:
                print container
        write(raw,port,block=True)
        check_response(port)

def do_cmd(port, opcode, data=[]):
        container = cmd_container(opcode, data)
        raw = build(container)
        if port.debug_level == 2:
                print container
        write(raw, port,block=True)
        
def do_tx(port,channel=0, payload_len=10, pattern='psn9'):
        container = tx_container(channel,payload_len,pattern)
        build_write_check(port, container)
        
def do_rx(port,channel=0):
        container = rx_container(channel)
        build_write_check(port,container)
        
def do_test_end(port):
        container = cmd_container('test_end')
        build_write_check(port,container)
        return parse(port.last_rx).event_params.cmd_response.pkt_count

def do_reset(port):
        do_cmd(port, 'util_reset')

from utils import *
from construct import Container, MappingError
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
                
def write(data, target):
        target.last_tx = data
        if target.debug:
                print "Sent: %s" % pretty(target.last_tx)

        #todo: replace with isinstance()
        if target.__class__.__name__ == 'Serial':
                target.has_data.clear()
                target.write(data)
                target.has_data.wait()
                
        if target.__class__.__name__ == 'modSocket':
                target.sendall(data)
                target.last_rx = target.recv(1024)

        if target.debug:
                print "Got:  %s\n" % pretty(target.last_rx)
         
def hand_code(input,port):
        write(pack(input), port)

def check_response(port):      
        
        def chat():
                if port.debug:
                        print "Success"
        try:
                response = parse(port.last_rx)
        except MappingError:
                print "Fault:"
                print "%s" % pretty(port.last_rx)
                raise
        
        if response.event_opcode == 'cmd_complete':
                if response.event_params.cmd_response.status == 'success':
                        chat()
                        return
                                
        if response.event_opcode == 'vendor_specific':
                if response.event_params.vendor_event_opcode == 'cmd_status':
                        if response.event_params.vendor_event_params.status == 'success':
                                chat()
                                return


def build_write_check(port,container):
        raw = build(container)
        write(raw, port)
        check_response(port)

def do_cmd(port, opcode, data=[]):
        container = cmd_container(opcode, data)
        build_write_check(port, container)
        
def do_tx(port,channel=0, payload_len=10, pattern='psn9'):
        container = tx_container(channel,payload_len,pattern)
        build_write_check(port, container)
        
def do_rx(port,channel=0):
        container = rx_container(channel)
        build_write_check(port, container)
        
def do_test_end(port):
        container = cmd_container('test_end')
        build_write_check(port,container)
        return parse(port.last_rx).event_params.cmd_response.pkt_count

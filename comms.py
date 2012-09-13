import serial
import socket
import threading
from utils import pretty
from serial.tools import list_ports

def setup_serial_port(port_path, socket=None, debug=False):
    port = serial.Serial()
    port.port = port_path
    port.baudrate = 57600 #specs from TI LE PTM guide
    port.rtscts = True
    port.parity = serial.PARITY_NONE
    port.bytesize = serial.EIGHTBITS
    port.stopbits = serial.STOPBITS_ONE
    port.timeout = 3 #blocking mode
    # non-standard fields #
    port.debug = debug
    port.has_data = threading.Event() #simple blocking system, false by default
    port.socket = socket
    port.last_rx = ''
    port.last_tx = ''
    
    port.open()
    return port

def reader(port):
    
    while port.isOpen():
        data = ''
        length = 0
        
        data = port.read(1) #blocks here

        if not data:
            continue
        
        if data == '\x04': #event pkt
            data = data + port.read(1) #event opcode, un-needed
            length = port.read(1) #read byte length
            data = data + length #append it to stream
            length = ord(length) #get int

            for i in range(0,length):
                data = data + port.read(1) #the rest

            port.last_rx = data
            port.has_data.set()
            if port.socket:
                port.socket.sendall(data)
            if port.debug:
                print "Got:  %s\n" % pretty(port.last_rx)
                    
        else:
            pass #types 1,2,3 not applicable


class modSocket(socket.socket):
    last_rx = ''
    last_tx = ''
    debug = False

def start_server(address='',tcp_port=2347):
    host = address #'' = all local interfaces
    port = tcp_port #arbitrary > 1000

    sock = modSocket(socket.AF_INET,
                     socket.SOCK_STREAM)
    
    sock.bind((host, port))
    sock.listen(1)
    conn, addr = sock.accept()
    return conn

def writer(port):
    while True:
        rx_data = port.socket.recv(1024)
        if not rx_data:
            break
        port.write(rx_data)
        port.last_tx = rx_data
        if port.debug:
            print "Sent: %s" % pretty(port.last_tx)

    port.socket.close()

def open_socket(host, tcp_port, debug=False):
        sock = modSocket(socket.AF_INET,
                         socket.SOCK_STREAM)
        sock.debug = debug
        sock.connect((host, tcp_port))
        return sock

def find_dongle(): #posix servers only
    matches = []
    for port in list_ports.grep('ACM'):
        matches.append(port[0])

    if len(matches) != 1:
        print "Multiple Dongles Found"

    return matches[0]

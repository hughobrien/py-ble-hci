import serial
import utils
import structs

def setup_serial_port(port_path):
    port = serial.Serial()
    port.port = port_path
    port.baudrate = 57600 #specs from TI LE PTM guide
    port.rtscts = True
    port.parity = serial.PARITY_NONE
    port.bytesize = serial.EIGHTBITS
    port.stopbits = serial.STOPBITS_ONE
    port.timeout = None #0 = non-blocking mode
    port.rxing = False #simple blocking system
    port.last_rx = ''
    port.last_tx = ''
    return port

def reader(port):
    while port.isOpen():
        data = ''
        length = 0
        
        data = port.read(1) #blocks here
        
        if data == '\x04': #event pkt
            data = data + port.read(1) #event opcode, un-needed
            length = port.read(1) #read byte length
            data = data + length #append it to stream
            length = ord(length) #get int

            for i in range(0,length):
                data = data + port.read(1) #the rest

            port.last_rx = data
            print "Got: %s\n%s" % (utils.pretty(data), repr(structs.parse(data)))

        else:
            print "Non event packet, %s. Aborting read loop." % data

        port.rxing = False #unblock
            

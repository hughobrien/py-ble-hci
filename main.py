from scripting import *
import comms
import threading

port = comms.setup_serial_port()
port.close()
port.open()

threading.Thread(target=comms.reader, args=(port,)).start()
print "Ready"

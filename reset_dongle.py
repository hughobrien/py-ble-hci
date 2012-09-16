import comms
import sys
import threading
from scripting import do_cmd

def reset_dongle(dongle):
        #Performs full HW reset, seems to trigger an OS re-enumeration
        #of the serial device, which means the old handle (e.g. COM1) changes,
        #but only sometimes...
        port = comms.setup_serial_port(dongle, debug=True)
        read_thread = threading.Thread(target=comms.reader, args=(port,))
        read_thread.start()
        do_cmd(port, 'util_reset')
        port.close()
        read_thread.join()


dongle = str(sys.argv[1])
reset_dongle(dongle)

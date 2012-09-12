import sys
import comms
import threading

#dongle = "/dev/ttyACM0" #posix style
#dongle = "\\.\COM5" #nt style

dongle = str(sys.argv[1])
tcp_port = int(sys.argv[2])

while True:
    port = comms.setup_serial_port(dongle, debug=True)
    port.socket = comms.start_server(tcp_port=tcp_port)

    read_thread = threading.Thread(target=comms.reader, args=(port,))
    write_thread = threading.Thread(target=comms.writer, args=(port,))

    write_thread.start() #start order not significant
    read_thread.start()

    write_thread.join() #write terminates first, by remote socket close

    port.close()

    read_thread.join() #read terminates on serial port close
    
    #up the spout again...

import socket
import os
from datetime import datetime
import time
import threading

SERVER_IP   = "192.168.1.104" 
EXO_IP      = "192.168.1.103"  
SERVER_PORT = 5013
EXO_PORT    = 5011
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((SERVER_IP, SERVER_PORT))

print("UDP server up and listening")

# datetime object containing current date and time
now = datetime.now()
# dd-mm-YY_H-M-S
dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

filename = "exoskeleton_data.csv"
f = open(filename, "w+")
#f.write("value_elbow, motor_current, timestamp\n")


def send_nudge():
    print("Started send_nudge")
    while(True):
        MSG = input()
        if (MSG == 'u'):
            UDPServerSocket.sendto(str.encode("up"),(EXO_IP,EXO_PORT))
        if (MSG == 'd'):
            UDPServerSocket.sendto(str.encode("down"),(EXO_IP,EXO_PORT))

# Listen for incoming datagrams
try:
    #send_nudge_thread = threading.Thread(target=send_nudge,args=())
    #send_nudge_thread.daemon = True
    #send_nudge_thread.start()
    while(True):
        message = UDPServerSocket.recvfrom(bufferSize)[0]
        decodedMessage = str(message, 'utf-8')
        formattedMessage = "{}\n".format(decodedMessage)
        # Save in a text file
        f.write(formattedMessage)
        print(formattedMessage)
        time.sleep(0.01)

except KeyboardInterrupt:
    UDPServerSocket.close()
    f.close()
    print("Closed server")
#!/usr/bin/env python
import time     # import the time library for the sleep function
from datetime import datetime
import threading
import logging
import socket
import os
import Motor_control as motor

print("Setting up logging...")
logging.basicConfig(filename='exoskeleton.log', filemode="w", format='%(message)s')
logging.info("value_elbow,current,timestamp")
print("Logging is set up!")

print("Setting up UDP connection...")

# Unity program
SERVER_IP = '192.168.0.104'
SERVER_PORT = 5013

# Exoskeleton
CLIENT_IP = '192.168.0.103'
CLIENT_PORT = 5011
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((CLIENT_IP, CLIENT_PORT))
print("UDP connection set up!")

print("Sending test UDP message...")
sock.sendto(str.encode("from pi"), (SERVER_IP, SERVER_PORT))

def executeNudging(direction: str):
        if direction == "up":
                target = 90
                motor.move_stepper(target)
                time.sleep(0.5)

        elif direction == "down":
                target = 0
                motor.move_stepper(target)
                time.sleep(0.5)
 
def messageCallback(data):
        message = data.decode("utf-8")

        if message == 'time':
                date_str = str(message.payload.decode("utf-8"))
                print("date:")
                print(date_str)
                os.system('sudo date -s %s' % date_str)

        if message == 'up' or message == 'down':
                actuateThread = threading.Thread(target=executeNudging, args=(message,))
                actuateThread.start()

def receiveMsg():
        while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                if (addr[0] == SERVER_IP):
                        messageCallback(data)

def main():
        try:
                # Starting a thread which is listening to the UDP messages until the program is closed
                receiveMsgThread = threading.Thread(target=receiveMsg, args=())
                receiveMsgThread.daemon = True # Making the Thread daemon so it stops when the main program has quit
                receiveMsgThread.start()

                print("Logging motor value and ready to take nudging messages through UDP")
                while True:
                        timeStamp = datetime.now().strftime('%H:%M:%S.%f')
                        value_elbow = motor.get_stepper_angle()
                        value_elbow = str(value_elbow)
                        current = motor.measure_current()
                        current = str(current)
                        udp_message = str.encode(f"{value_elbow}, {timeStamp}")
                        print(udp_message)
                        sock.sendto(udp_message, (SERVER_IP, SERVER_PORT))

                        logging.info(value_elbow + "," + current + "," + timeStamp)
                        time.sleep(0.01) # Without sleep the system logs and sends data to

        except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard
                sock.close()
                print('\nsocket closed')
                motor.release() # Releasing motor and GPIO pins
                logging.info("program stopped")
                print('Program stopped')

if __name__ == "__main__":
    main()
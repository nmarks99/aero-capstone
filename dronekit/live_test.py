#!/usr/bin/env python3
import time
import os
import dronekit 
import dklib

def connect():
    PORT = "/dev/serial0"
    BAUDRATE = 921600 # check

    print("Connecting...")
    #  vehicle = dronekit.connect(PORT, baud=BAUDRATE, wait_ready=True)
    print('Connected Successfully!')
    #  print(vehicle.version)
    input("Press enter to continue")
    #  return vehicle

def clear():
    os.system("clear || cls")

arg_dict = {
    "connect":connect,
    "clear":clear,
}



while True:
    arg = input("DroneKit >> ")
    arg = arg.split(" ")

    if arg[0] == "close":
        break
    else:
        arg_dict[arg[0]]()






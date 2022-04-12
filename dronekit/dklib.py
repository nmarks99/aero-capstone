#!/usr/bin/env python3
import dronekit
import time 

def connect_drone(CONNECTION_STRING,BAUDRATE=115200):
    print("Connecting...")
    try:
        vehicle = dronekit.connect(CONNECTION_STRING,BAUDRATE,wait_ready=True)
    except:
        print("Failed to connect")
    print("Connection Established")
    return vehicle


# Close vehicle object before exiting script
# vehicle.close()

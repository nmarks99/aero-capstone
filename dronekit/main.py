#!/usr/bin/env python3


'''
main script for running dronekit
'''

import dronekit
import dklib
import time
from dklib import clear_print

# Define connection port and baudrate
PORT = "/dev/serial0" # Serial port on the Pi
BAUD = 921600

# Connect to the drone
clear_print("Connecting...")
vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
clear_print("Connected Successfully!\n\n")

input("Press enter to continue")

#  vehicle.mode = dronekit.VehicleMode("GUIDED")
vehicle.armed = True

# Set the servo position
dklib.set_servo(vehicle, 9, "low")
time.sleep(1)
dklib.set_servo(vehicle, 9, "mid")
time.sleep(1)
dklib.set_servo(vehicle, 9, "high")

while True:
    clear_print(vehicle.attitude)
    time.sleep(0.1)

# Close vehicle object
vehicle.close()

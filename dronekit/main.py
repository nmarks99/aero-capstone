#!/usr/bin/env python3


'''
main script for running dronekit
'''

import dronekit
import dklib
from dklib import clear_print

# Define connection port and baudrate
PORT = "/dev/serial0" # Serial port on the Pi
BAUD = 921600

# Connect to the drone
clear_print("Connecting...")
vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
clear_print("Connected Successfully!\n\n")

# Set the servo position
dklib.set_servo(vehicle, 9, "mid")

# Close vehicle object
vehicle.close()

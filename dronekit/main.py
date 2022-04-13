#!/usr/bin/env python3


'''
main script for running dronekit
'''

import dronekit
import dklib
from dklib import clear_print

# Connect to the drone
clear_print("Connecting...")
vehicle = dronekit.connect("com5", baud=115200, wait_ready=True)
clear_print("Connected Successfully!\n\n")

# Set the servo position
dklib.set_servo(vehicle, 9, "mid")

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

# Connect to the Pixhawk
clear_print("Connecting...")
vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
clear_print("Connected Successfully!\n\n")
input("Press enter to continue")

# Arm the vehicle
while not vehicle.armed:
    clear_print("Waiting to arm...")
    vehicle.armed = True
    time.sleep(1)

# Takeoff and go to a target altitude
print("Taking off!")
TARGET_ALT = 3 # meters
dklib.takeoff(vehicle, TARGET_ALT)

# Hover at this spot for 
hover_time = 3 # 3 seconds 
dklib.set_attitude(duration=hover_time)

# Land 
print("Landing...")
vehicle.mode = dronekit.VehicleMode("LAND")
time.sleep(1)

# Close vehicle object
vehicle.close()
clear_print("Mission complete")

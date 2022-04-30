#!/usr/bin/env python3



import dronekit
import dklib
import time
from dklib import clear_print

# Define connection port and baudrate
PORT = "/dev/serial0" # Serial port on the Pi
BAUD = 921600

# Connect to the drone
clear_print("Connecting...")
vehicle = dronekit.connect(PORT, baud=BAUD)
clear_print("Connected Successfully!\n\n")

input("Press enter to continue")

#  vehicle.mode = dronekit.VehicleMode("GUIDED")
vehicle.armed = True
time.sleep(5)

# Close vehicle object
vehicle.close()

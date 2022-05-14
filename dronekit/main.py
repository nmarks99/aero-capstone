#!/usr/bin/env python3

import dronekit
import dklib
import time
import imu
from dklib import clear_print

"""
SETUP
"""

# Define connection port and baudrate
PORT = "/dev/serial0" # Serial port on the Pi
BAUD = 921600

# Connect IMU
IMU = imu.connect_imu()

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
    print("Armed!")





"""
MAIN PROGRAM LOOP
"""
acc_data = [] 
DROPPED = False # Flag for if drop has been detected or not
DROP_THRESHOLD = 1234 # TODO: update thresholds
HOVER_THRESHOLD = 1234
ARM_SERVO = 9
LEG_SERVO = 10 # TODO: check servo number

t0 = time.time() # time = 0 here

# Waiting for drop to be detected 
while True:
    t_now = time.time() - t0
    
    ax = IMU.acceleration[0]
    ay = IMU.acceleration[1]
    az = IMU.acceleration[2]
    acc_data.append((ax,ay,az), t_now)
    
    if az >= DROP_THRESHOLD:
        clear_print("Drop detected!...Deploying arms")
        dklib.set_servo(vehicle, ARM_SERVO, "HIGH")
        time.sleep(0.1) # TODO: check this sleep
        break

    time.sleep(0.05) # TODO: is this a good delay?


# Drop detected, waiting to reach hover
while True:
    
    t_now = time.time() - t0
   
    ax = IMU.acceleration[0]
    ay = IMU.acceleration[1]
    az = IMU.acceleration[2]
    acc_data.append((ax,ay,az), t_now)
    
    # Set thrust to max
    dklib.set_attitude(thrust=1.0)
    
    if az <= HOVER_THRESHOLD:
        clear_print("Hover reached!")
        dklib.set_servo(vehicle, LEG_SERVO, "HIGH")
        break
    
    time.sleep(0.05)
   
# Set to land mode 
vehicle.mode = dronekit.VehicleMode("LAND")
input("Press enter when complete")

# Save acceleration data
imu.write_to_file(acc_data)

# Close vehicle object
vehicle.close()

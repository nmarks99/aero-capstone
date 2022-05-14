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
# Define constants
DROPPED = False # Flag for if drop has been detected or not
DROP_THRESHOLD = 1234 # TODO: update thresholds
HOVER_THRESHOLD = 1234
ARM_SERVO = 9
LEG_SERVO = 10 # TODO: check servo number

t0 = time.time() # time = 0 here
acc_data = [] # array to store acceleration data 

try:
    while True:
        
        # Get current time and acceleration
        t_now = time.time() - t0
        (ax, ay, az, amag) = imu.read_acc(IMU)
        acc_data.append([ax, ay, az, amag, t_now]) 

        # Print out acceleration data
        print(
            "ax = {:.3f}\tay = {:.3f}\taz = {:.3f}\tamag = {:.3f}\tt = {:.3f} s"
            .format(ax,ay,az,amag,t_now)
        )
        

        if not DROPPED:
            # Check if drop detected
            if amag >= DROP_THRESHOLD:
                DROPPED = True
                 
                # Deploy arms
                print("Arms deployed")
                dklib.set_servo(vehicle, ARM_SERVO, "HIGH")
                
                # Set throttle to 100%
                print("Throttle set to 100%")
                dklib.set_attitude(thrust=1.0)
        
        # Check if hover detected
        elif DROPPED:
            # Keep throttle at max until hover is detected
            dklib.set_attitude(thrust=1.0)
            
            if amag <= HOVER_THRESHOLD:
                print("Hover achieved!")

                # Deploy legs
                # Hold position for 2 seconds
                print("Legs deployed")
                dklib.set_servo(vehicle, LEG_SERVO, "HIGH")
                dklib.set_attitude(duration=2) # TODO: Check if this works
                
                # Set to LAND mode
                vehicle.mode = dronekit.VehicleMode("LAND")
                break # Break out of the loop when we switch to LAND

        time.sleep(0.05) # TODO: check if this delay is sufficient

    time.sleep(10) # TODO: Check the time here
    print("Mission Complete")
    
    # Close vehicle object
    vehicle.close()

except KeyboardInterrupt:
    # Write the acceleration data to a file
    imu.write_to_file(acc_data)
    pass # TODO: add code to safely abort mission


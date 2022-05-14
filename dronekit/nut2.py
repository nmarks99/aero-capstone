#!/usr/bin/env python3

import dronekit
import dklib
import time
import imu
from dklib import clear_print




def arm_and_takeoff_nogps(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude without GPS data.
    """

    ##### CONSTANTS #####
    DEFAULT_TAKEOFF_THRUST = 0.7
    SMOOTH_TAKEOFF_THRUST = 0.6

    #  print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    # If you need to disable the arming check,
    # just comment it with your own responsibility.
    #  while not vehicle.is_armable:
        #  print(" Waiting for vehicle to initialise...")
        #  time.sleep(1)

    #  print("Arming motors")
    # Copter should arm in GUIDED_NOGPS mode
    vehicle.mode = VehicleMode("GUIDED_NOGPS")
    #  vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        vehicle.armed = True
        time.sleep(1)

    print("Taking off!")

    thrust = DEFAULT_TAKEOFF_THRUST
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(" Altitude: %f  Desired: %f" %
              (current_altitude, aTargetAltitude))
        if current_altitude >= aTargetAltitude*0.95: # Trigger just below target alt.
            print("Reached target altitude")
            break
        elif current_altitude >= aTargetAltitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(thrust = thrust)
        time.sleep(0.2)






"""
SETUP
"""

# Define connection port and baudrate
PORT = "/dev/serial0" # Serial port on the Pi
BAUD = 921600

# Connect to the Pixhawk
clear_print("Connecting...")
vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
clear_print("Connected Successfully!\n\n")
input("Press enter to continue")

# Connect IMU
IMU = imu.connect_imu()

# vehicle.mode = dronekit.VehicleMode("GUIDED_NOGPS")

# # Arm the vehicle
# while not vehicle.armed:
#     clear_print("Waiting to arm...")
#     vehicle.armed = True
#     time.sleep(1)
#     print("Armed!")


"""
MAIN PROGRAM LOOP
"""
# Define constants
DROPPED = False # Flag for if drop has been detected or not
DROP_THRESHOLD = 1 # TODO: update thresholds
HOVER_THRESHOLD = 1
ARM_SERVO = 9
LEG_SERVO = 10 # TODO: check servo number

# Take off in GUIDED_NOGPS mode.
print("Taking off...")
# dklib.takeoff(vehicle, target_altitude=5.0)
arm_and_takeoff_nogps(5)

# Hold the position for 3 seconds.
print("Holding position for 3 seconds")
dklib.set_attitude(duration = 3)

# Cut motors
print("Cut motors")
dklib.set_attitude(thrust=0.0)
time.sleep(0.2)

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

            elif vehicle.location.global_relative_frame.alt <= 3.0:
                print("PANIC! ABORT MISSION!")
                dklib.set_attitude(thrust=1.0)
                time.sleep(0.5)
                vehicle.mode = dronekit.VehicleMode("ALT_HOLD")
        
        # Check if hover detected
        elif DROPPED:
            # Keep throttle at max until hover is detected
            dklib.set_attitude(thrust=1.0)
            
            if amag <= HOVER_THRESHOLD or vehicle.location.global_relative_frame.alt > 5:
                print("Hover achieved!")

                # Deploy legs
                # Hold position for 2 seconds
                # print("Legs deployed")
                # dklib.set_servo(vehicle, LEG_SERVO, "HIGH")

                # Hold altitude here
                vehicle.mode = dronekit.VehicleMode("ALT_HOLD")
                time.sleep(5)

                # dklib.set_attitude(duration=2) # TODO: Check if this works
                
                # Set to LAND mode
                vehicle.mode = dronekit.VehicleMode("LAND")
                break # Break out of the loop when we switch to LAND

        time.sleep(0.05) # TODO: check if this delay is sufficient

    imu.write_to_file(acc_data) # save imu data
    time.sleep(10) # TODO: Check the time here
    print("Mission Complete")
    
    # Close vehicle object
    vehicle.close()

except KeyboardInterrupt:
    # Write the acceleration data to a file
    vehicle.mode = dronekit.VehicleMode("LAND")
    imu.write_to_file(acc_data)


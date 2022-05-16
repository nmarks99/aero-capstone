#!/usr/bin/env python3

import dronekit
from math import sqrt
import dklib
import time
import imu
from utils import clear_print, color_print


def main():

    """
    SETUP
    """

    # Define connection port and baudrate
    PORT = "/dev/serial0" # Serial port on the Pi
    BAUD = 921600

    # Connect to the Pixhawk
    clear_print("Connecting...")
    vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
    color_print("Connected Successfully!\n\n","BOLD_RED")
    input("Press enter to continue")

    # Connect IMU
    IMU = imu.connect_imu()

    # Set vehicle mode to GUIDED_NOGPS
    vehicle.mode = dronekit.VehicleMode("GUIDED_NOGPS")

    # Arm the vehicle
    while not vehicle.armed:
        clear_print("Waiting to arm...")
        vehicle.armed = True
        time.sleep(1)
        color_print("Armed","BOLD_RED")


    """
    MAIN PROGRAM LOOP
    """
    # Define constants
    DROPPED = False # Flag for if drop has been detected or not
    DROP_THRESHOLD = 8.8 # TODO: update thresholds
    HOVER_THRESHOLD = 8.8
    ARM_SERVO = 9
    LEG_SERVO = 10 # TODO: check servo number

    # Take off in GUIDED_NOGPS mode.
    print("Taking off...")
    TAKEOFF_ALTITUDE = 5
    dklib.takeoff(vehicle,target_altitude=TAKEOFF_ALTITUDE)

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
            # t_now = time.time() - t0
            # (ax, ay, az, amag) = imu.read_acc(IMU)


            # Trying this instead of the read_acc function
            t_now = time.time() - t0
            ax = IMU.acceleration[0]
            ay = IMU.acceleration[1]
            az = IMU.acceleration[3]
            amag = sqrt(ax**2 + ay**2 + az**2)
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
                    color_print("PANIC! ABORT MISSION!","BOLD_RED")
                    dklib.set_attitude(thrust=1.0)
                    time.sleep(0.5)
                    vehicle.mode = dronekit.VehicleMode("ALT_HOLD")
            
            # Check if hover detected
            elif DROPPED:
                # Keep throttle at max until hover is detected
                dklib.set_attitude(thrust=1.0)
                
                if amag <= HOVER_THRESHOLD or vehicle.location.global_relative_frame.alt >= TAKEOFF_ALTITUDE:
                    print("Hover achieved!")

                    # Deploy legs
                    # Hold position for 2 seconds
                    color_print("Legs deployed","BOLD_RED")
                    dklib.set_servo(vehicle, LEG_SERVO, "HIGH")

                    # Hold altitude here
                    vehicle.mode = dronekit.VehicleMode("ALT_HOLD")
                    time.sleep(5)
                    
                    # Set to LAND mode
                    vehicle.mode = dronekit.VehicleMode("LAND")
                    break # Break out of the loop when we switch to LAND

            time.sleep(0.05) # TODO: check if this delay is sufficient

        imu.write_to_file(acc_data) # save imu data
        time.sleep(5) # TODO: Check the time here
        print("Mission Complete")
        
        # Close vehicle object
        vehicle.close()


    except KeyboardInterrupt:
        color_print("KEYBOARD INTERRUPT\nABORTING MISSION\nLANDING...","BOLD_RED")
        
        # Set vehicle to land
        vehicle.mode = dronekit.VehicleMode("LAND")
        time.sleep(5)

        # Write the acceleration data to a file
        imu.write_to_file(acc_data)

        # Close vehicle object
        vehicle.close()





if __name__ == "__main__":
    main()

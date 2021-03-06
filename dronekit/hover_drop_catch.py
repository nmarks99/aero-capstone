#!/usr/bin/env python3
import sys; sys.path.append("../")
import dronekit
from math import sqrt
import dklib
import time
import imu
from utils import brint 
import threading


def main():

    """
    SETUP
    """

    # Define connection port and baudrate
    PORT = "/dev/serial0" # Serial port on the Pi
    BAUD = 921600

    # Connect to the Pixhawk
    brint("Connecting...",clear=True)
    vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
    brint("Connected Successfully!\n\n",color="BOLD_RED")
    input("Press enter to continue")

    # Set vehicle mode to GUIDED_NOGPS
    vehicle.mode = dronekit.VehicleMode("GUIDED_NOGPS")

    # Arm the vehicle
    while not vehicle.armed:
        brint("Waiting to arm...",clear=True)
        vehicle.armed = True
        time.sleep(1)
        brint("Armed",color="BOLD_RED")

    # Read IMU data in a separate thread and store it in a list
    # Format is [[ax,ay,az,amag,timestamp]]
    stop_thread = threading.Event()
    acc_data = []
    imu_thread = threading.Thread(target=imu.imu_thread_func,args=(acc_data,stop_thread,))
    imu_thread.start()


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

    try:
        
        while True:
            
            # Get acceleration magnitude from the acc_data array
            # last list is the most recent since its running in parallel 
            if len(acc_data) > 0:
                try:
                    ax = round(acc_data[-1][0],4)
                    ay = round(acc_data[-1][1],4)
                    az = round(acc_data[-1][2],4)
                    t = acc_data[-1][3]
                    amag = sqrt(ax**2 + ay**2 + az**2)
                    
                    # Print out acceleration data
                    print(
                        "ax = {:.3f}\tay = {:.3f}\taz = {:.3f}\tamag = {:.3f}\tt = {:.3f} s"
                        .format(ax,ay,az,amag,t)
                    )

                except:
                    brint("Missed IMU data point",color="BOLD_RED")
                    

            if not DROPPED:
                # Check if drop detected
                if amag >= DROP_THRESHOLD:
                    DROPPED = True
                    
                    # Deploy arms
                    brint("Arms deployed",color="BOLD_RED")
                    dklib.set_servo(vehicle, ARM_SERVO, "HIGH")
                    
                    # Set throttle to 100%
                    brint("Throttle set to 100%",color="BOLD_RED")
                    dklib.set_attitude(thrust=1.0)

                elif vehicle.location.global_relative_frame.alt <= 3.0:
                    brint("PANIC! ABORT MISSION!",color="BOLD_RED")
                    dklib.set_attitude(thrust=1.0)
                    time.sleep(0.5)
                    vehicle.mode = dronekit.VehicleMode("ALT_HOLD")
            
            # Check if hover detected
            elif DROPPED:
                # Keep throttle at max until hover is detected
                dklib.set_attitude(thrust=1.0)
                
                if amag <= HOVER_THRESHOLD or vehicle.location.global_relative_frame.alt >= TAKEOFF_ALTITUDE:
                    brint("Hover achieved",color="BOLD_RED")

                    # Deploy legs
                    # Hold position for 2 seconds
                    brint("Legs deployed",color="BOLD_RED")
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
        brint("Mission Complete",color="BOLD_GREEN")
        
        # Close vehicle object
        vehicle.close()


    except KeyboardInterrupt:
        brint("KEYBOARD INTERRUPT\nABORTING MISSION\nLANDING...",color="BOLD_RED")
        
        # Set vehicle to land
        vehicle.mode = dronekit.VehicleMode("LAND")
        time.sleep(5)

        # Write the acceleration data to a file
        imu.write_to_file(acc_data)

        # Close vehicle object
        vehicle.close()


    # Stop the thread and write the IMU data to a text file
    stop_thread = True
    imu_thread.join()
    imu.write_to_file(acc_data)


if __name__ == "__main__":
    main()



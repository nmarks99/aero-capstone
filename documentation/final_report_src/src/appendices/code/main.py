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
    HOVER_THRESHOLD = 9.8
    ARM_SERVO = 9

    try:
        
        while True:
            
            # Get acceleration magnitude from the acc_data array
            # last list is the most recent since its running in parallel 
            if len(acc_data) > 0: # wait until we have data

                ax = round(acc_data[-1][0],4)
                ay = round(acc_data[-1][1],4)
                az = round(acc_data[-1][2],4)
                amag = round(acc_data[-1][3],4)
                t = round(acc_data[-1][4],4)
                

                if not DROPPED:
                    
                    # Print out acceleration data
                    brint("",clear=True)
                    print("Dropped = ",end="")
                    brint("False",color="BOLD_RED") 

                    # Check if drop detected
                    if amag >= DROP_THRESHOLD:
                        DROPPED = True
                        
                        # Deploy arms and legs
                        dklib.set_servo(vehicle, ARM_SERVO, "HIGH")
                
                        brint("",clear=True)
                        print("Dropped = ",end="")
                        brint("True",color="BOLD_GREEN")
                        break

                elif DROPPED:

                    # Set thrust to maximum until hover is reached
                    while True:
                        dklib.set_attitude(thrust=1.0)
                        if abs(amag-HOVER_THRESHOLD) < 0.9*HOVER_THRESHOLD:
                            brint("Hover Reached!",color="BOLD_GREEN")
                            break
                        else:
                            time.sleep(0.1)

                    # Set vehicle to LAND mode
                    vehicle.mode = dronekit.VehicleMode("LAND")
                    time.sleep(10)



                print(
                    "ax = {:.3f}\tay = {:.3f}\taz = {:.3f}\tamag = {:.3f}\tt = {:.3f} s"
                    .format(ax,ay,az,amag,t)
                )
                
                time.sleep(0.05) # TODO: check if this delay is sufficient


        brint("Mission Complete",color="BOLD_GREEN")
        
        # Close vehicle object
        input("Press enter to close vehicle object")
        vehicle.close()

    except KeyboardInterrupt:
        brint("KEYBOARD INTERRUPT\nABORTING MISSION",color="BOLD_RED")
        
        # Close vehicle object
        vehicle.close()


    # Stop the thread and write the IMU data to a text file
    stop_thread.set()
    imu_thread.join()
    imu.write_to_file(acc_data)


if __name__ == "__main__":
    main()



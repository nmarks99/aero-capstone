#!/usr/bin/env python3

import dronekit
from math import sqrt
import dklib
import time
import imu
from utils import clear_print, color_print
import threading



def main():
    
    try:
        # Define connection port and baudrate
        PORT = "/dev/serial0" # Serial port on the Pi
        BAUD = 921600

        # Connect to the Pixhawk
        color_print("Connecting...", "BOLD_RED",clear=True)
        vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
        color_print("Connected Successfully!\n\n","BOLD_RED")
        input("Press enter to continue")

        # Read IMU data in a separate thread and store it in a list
        # Format is [[ax,ay,az,amag,timestamp]]
        stop_thread = threading.event()
        data_arr = []
        imu_thread = threading.Thread(target=imu.imu_thread_func,args=(data_arr,stop_thread,))
        imu_thread.start()

        # Set vehicle mode to GUIDED_NOGPS
        vehicle.mode = dronekit.VehicleMode("GUIDED_NOGPS")

        # Arm the vehicle
        while not vehicle.armed:
            color_print("Waiting to arm...","BOLD_RED",clear=True)
            vehicle.armed = True
            time.sleep(1)
            color_print("Armed","BOLD_RED")

        # Take off in GUIDED_NOGPS mode.
        color_print("Taking off...","BOLD_RED")
        TAKEOFF_ALTITUDE = 2
        dklib.takeoff(vehicle,target_altitude=TAKEOFF_ALTITUDE,default_takeoff_thrust=1.0)

        # Hold the position for 3 seconds.
        print("Holding position for 3 seconds")
        dklib.set_attitude(vehicle,duration = 3)
        
        # Land
        vehicle.mode = dronekit.VehicleMode("LAND")

        # Close when user is ready
        color_print("Mission Complete. Press enter to close vehicle", "BOLD_GREEN")
        input("")
        vehicle.close()


    except KeyboardInterrupt:
        color_print("PANIC! ABORT MISSION")
        vehicle.mode = dronekit.VehicleMode("LAND")
        time.sleep(2)
        while True:
            dklib.set_attitude(thrust=0.0)
            time.sleep(1)
    
    # Stop the thread and write the IMU data to a text file
    stop_thread.set()
    imu_thread.join()
    imu.write_to_file(data_arr)


if __name__ == "__main__":
    main()




#!/usr/bin/env python3

import dronekit
from math import sqrt
import dklib
import time
import imu
from utils import clear_print, color_print
import threading

def main():
    
    stop_thread = False
    # Connect IMU and make a thread function
    IMU = imu.connect()
    t0 = time.time()
    def imu_thread_func(data_arr):
        while True:
            t = time.time() - t0
            ax,ay,az,amag = imu.read_acc(IMU)
            
            # Print out acceleration data
            print(
                "ax = {:.3f}\tay = {:.3f}\taz = {:.3f}\tamag = {:.3f}\tt = {:.3f} s"
                .format(ax,ay,az,amag,t)
            )
            data_arr.append([ax,ay,az,amag,t])
            global stop_thread
            if stop_thread:
                break

    stop_thread = False
    data_arr = []
    imu_thread = threading.Thread(target=imu_thread_func,args=(data_arr,))
    imu_thread.start()

    try:
        # Define connection port and baudrate
        PORT = "/dev/serial0" # Serial port on the Pi
        BAUD = 921600

        # Connect to the Pixhawk
        clear_print("Connecting...")
        vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
        color_print("Connected Successfully!\n\n","BOLD_RED")
        input("Press enter to continue")

        # Connect IMU
        #  IMU = imu.connect_imu()

        # Set vehicle mode to GUIDED_NOGPS
        vehicle.mode = dronekit.VehicleMode("GUIDED_NOGPS")

        # Arm the vehicle
        while not vehicle.armed:
            clear_print("Waiting to arm...")
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
        time.sleep(1)
        
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

    stop_thread = True
    imu_thread.join()


if __name__ == "__main__":
    main()




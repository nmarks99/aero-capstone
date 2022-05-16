#!/usr/bin/env python3

import dronekit
from math import sqrt
import dklib
import time
import imu
from utils import clear_print, color_print


def main():


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


    # Take off in GUIDED_NOGPS mode.
    color_print("Taking off...","BOLD_RED")
    TAKEOFF_ALTITUDE = 5
    dklib.takeoff(vehicle,target_altitude=TAKEOFF_ALTITUDE)

    # Hold the position for 3 seconds.
    print("Holding position for 3 seconds")
    dklib.set_attitude(duration = 3)

    # Land
    vehicle.mode = dronekit.VehicleMode("LAND")

    # Close when user is ready
    color_print("Mission Complete. Press enter to close vehicle", "BOLD_GREEN")
    input("")
    vehicle.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3



import dronekit
import dklib
import time
from dklib import clear_print
import argparse
import board
import busio
import adafruit_bno055
import time
from math import sqrt

# connect IMU
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Define connection port and baudrate
PORT = "/dev/serial0" # Serial port on the Pi
BAUD = 921600

# Connect to the drone
clear_print("Connecting...")
vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
clear_print("Connected Successfully!\n\n")

input("Press enter to continue")

#Damn thing wont play a tune

#parser = argparse.ArgumentParser(description='Play tune')
#parser.add_argument('--tune', type=str, help="tune to play", default="AAAA")
#args = parser.parse_args()

#vehicle.play_tune(args.tune)
#  vehicle.mode = dronekit.VehicleMode("GUIDED")
#vehicle.armed = True
time.sleep(1)

while(True):
    ax = sensor.acceleration[0]
    ay = sensor.acceleration[1]
    az = sensor.acceleration[2]
    a_mag = sqrt(ax**2 + ay**2 + az**2)
    time.sleep(0.05)
    print(a_mag)
    if a_mag < 5.0:
        print("Drop detected!")
        dklib.set_servo(vehicle,9, "high")
        break


dklib.set_servo(vehicle,9,1750)

# Close vehicle object
vehicle.close()

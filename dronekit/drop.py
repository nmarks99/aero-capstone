#!/usr/bin/env python3



import dronekit
import dklib
import time
from dklib import clear_print
import argparse

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
   v1=vehicle.velocity[2]
   time.sleep(0.04)
   v2=vehicle.velocity[2]
   accel = (v2 - v1)
   print(accel)
   if (abs(vehicle.velocity[0]) > 1.0 or abs(vehicle.velocity[1]) > 1.0 or abs(vehicle.velocity[2]) > 1.0):
      dklib.set_servo(vehicle,9,"high")
      dklib.set_servo(vehicle,9,"low")
      print("Drop Detected")
      print("Acceleration:{:.4f}".format(accel))
      print(vehicle.velocity[2])
      break
   time.sleep(0.01)
   
dklib.set_servo(vehicle,9,1750)

# Close vehicle object
vehicle.close()

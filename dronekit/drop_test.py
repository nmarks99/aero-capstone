#!/usr/bin/env python3
import dronekit
import dklib
import time
import sys 
sys.path.append("../")
from utils import brint
import time
import threading
import imu

# Define connection port and baudrate
PORT = "/dev/serial0" # Serial port on the Pi
BAUD = 921600

# Connect to the drone
brint("Connecting...",color="BOLD_YELLOW",clear=True)
vehicle = dronekit.connect(PORT, baud=BAUD, wait_ready=True)
brint("Connected Successfully!\n\n",color="BOLD_GREEN",clear=True)

# Stow arms and legs before starting 
dklib.set_servo(vehicle,9,"OPEN")
brint("Put arms in stowed position\nPress enter when done",color="BOLD_CYAN")
input("")
dklib.set_servo(vehicle,9,"CLOSE")
time.sleep(1)
brint("Stow legs\n Press enter when done",color="BOLD_CYAN",clear=True)
input("")
time.sleep(1)
brint("Press enter to initiate drop detection",color="BOLD_CYAN",clear=True)
input("")


stop_thread = threading.Event()
acc_data = []
imu_thread = threading.Thread(target=imu.imu_thread_func,args=(acc_data,stop_thread,))
imu_thread.start()


THRESHOLD = 0.9
last_len = 0
while(True):
    # Get acceleration component, msagnitude, and timestep
    if len(acc_data) > last_len:
        # only update new values for acceleration when they come in
        ax = round(acc_data[-1][0],3)
        ay = round(acc_data[-1][1],3)
        az = round(acc_data[-1][2],3)
        a_mag = round(acc_data[-1][3],3)
        t = round(acc_data[-1][4],3)
        last_len = len(acc_data)

        print("t = {}s\tax = {}\tay = {}\taz = {}\tmag = {}".format(t,ax,ay,az,a_mag))
    #  time.sleep(0.05) # Can potentially adjust this delay
     
    # If threshold for falling is met, deploy arms and break out
    if a_mag < THRESHOLD:
        brint("Drop detected!",color="BOLD_YELLOW")
        dklib.set_servo(vehicle,9, "HIGH")
        break

# Set servo back to its start 
time.sleep(1)
dklib.set_servo(vehicle,9,"OPEN")
imu.write_to_file(acc_data)

# Close vehicle object
vehicle.close()

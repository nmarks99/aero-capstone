#!/usr/bin/env python3
import dklib
import dronekit
import time


v = dronekit.connect("/dev/serial0",baud=921600,wait_ready=True)

input("Press enter to spin servo")
dklib.set_servo(v, 9, "LOW")
time.sleep(1)
dklib.set_servo(v, 9, "HIGH")
time.sleep(5)




#!/usr/bin/env python3
import dklib
import dronekit

v = dronekit.connect("/dev/serial0",baud=921600,wait_ready=True)

input("Press enter to spin servo")
dklib.set_servo(v, 9, "LOW")




#!/usr/bin/env python3
import dklib
import dronekit
from utils import color_print
import utils

utils.clear()
color_print("Connecting...", "BOLD_YELLOW")
v = dronekit.connect("/dev/serial0",baud=921600,wait_ready=True)
color_print("Connected!","BOLD_RED")

dklib.set_servo(v, 9, "HIGH")



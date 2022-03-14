#!/usr/bin/env python3
import random
import numpy as np
import os 
from datetime import datetime
import time
import sys

# Passing "debug" as an cmd line input argument will print random numbers instead 
# of actually reading load cell. Good for debugging.
FLAG = True
if len(sys.argv) == 2:
    if sys.argv[1] == "debug":
        FLAG = False
    else:
        try:
            throttle_val = float(sys.argv[1])
        except:
            raise ValueError("Input throttle value cannot be converted to float")
elif len(sys.argv) != 1:
    raise ValueError('Invalid number of inputs')


if FLAG:
    # only import RPI.GPIO and pigpio
    import RPi.GPIO as gpio
    import pigpio

    pi = pigpio.pi()
    ESC = 4 # ESC connected to GPIO pin #4
    pi.set_servo_pulsewidth(ESC,0) # initially set pulse width to zero


def throttle(val):
    '''
    throttle(val) sets pulse width for PWM signal given a value between 0 and 1
    corresponding to a percentage of max throttle
    '''

    assert(val >= 0 and val <= 1), 'Throttle is a value between 0(min) and 1 (max)'
    pulse_width = 1000 + 1000*val
    pi.set_servo_pulsewidth(ESC,pulse_width)
    

while(True): 
    throttle(throttle_val)
    throttle_val = input(">> ")
    time.sleep(0.05)

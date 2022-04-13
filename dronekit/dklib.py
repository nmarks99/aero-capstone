#!/usr/bin/env python3


'''
dklib.py 

Interal library of functions that use dronekit but are written by us
and taylored for our specific application.
'''

import dronekit
import os 


def clear_print(msg):
	os.system("clear || cls")
	print(msg)


def set_servo(vehicle, servo_number, pwm_value):
    
    assert(isinstance(pwm_value,int) or isinstance(pwm_value,str)),'pwm_value must be an integer between 1000 and 2000 or "low", "mid", and "high"'
    values = {
        "low": 1000,
        "mid": 1500,
        "high": 2000
    } 

    if isinstance(pwm_value,str):
        pwm_value = pwm_value.lower()
        pwm_value = values[pwm_value]
    else:
        pwm_value_int = int(pwm_value)
    
    msg = vehicle.message_factory.command_long_encode(
		0,
        0,
        dronekit.mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
		servo_number,
		pwm_value_int,
		0,0,0,0,0 # rest are zero
		)
        
    vehicle.send_mavlink(msg)

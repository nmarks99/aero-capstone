#!/usr/bin/env python3
import board
import busio
import adafruit_bno055
import time
from dklib import clear_print

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
    ax = sensor.acceleration[0]
    ay = sensor.acceleration[1]
    az = sensor.acceleration[2]
    clear_print(ax, ay, az)
    time.sleep(0.02)


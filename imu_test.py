import board
import busio
import adafruit_bno055
import time
from numpy import sqrt

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:

    ax = sensor.acceleration[0]
    ay = sensor.acceleration[1]
    az = sensor.acceleration[2]
    a_mag = sqrt(ax**2 + ay**2 + az**2)
    
  
    time.sleep(0.1)


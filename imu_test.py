import board
import busio
import adafruit_bno055
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
    print(sensor.acceleration)
    time.sleep(0.1)


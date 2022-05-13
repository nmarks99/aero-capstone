import board
import busio
import adafruit_bno055

def connect_imu():
    i2c = busio.I2C(board.SCL, board.SDA)
    imu = adafruit_bno055.BNO055_I2C(i2c)
    return imu
